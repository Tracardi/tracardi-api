import json
import logging
from typing import Optional

from app.api.auth.token_memory import TokenMemory
from tracardi.config import tracardi
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage import index
from tracardi.service.storage.driver import storage
from tracardi.service.storage.elastic_client import ElasticClient
from hashlib import sha1

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class TokenDb:

    def __init__(self):
        if tracardi.tokens_in_redis is False:
            self._elastic = ElasticClient.instance()
            self._index_write = index.resources['user'].get_write_index()

        else:
            self._token_memory = TokenMemory()

    async def delete(self, token: str):
        if tracardi.tokens_in_redis is False:
            query = {
                "query": {
                    "term": {"token": token}
                },
                "script": "ctx._source.token = null;"
            }

            await self._elastic.update_by_query(self._index_write, query)

        else:
            del self._token_memory[token]

    async def get(self, token) -> Optional[User]:

        # todo add caching

        if tracardi.tokens_in_redis is False:
            result = await storage.driver.user.search_by_token(token)
            if result.total > 1:
                raise ValueError(f"Invalid user count result. Expected 0 or 1 got {result.total}")

            result = list(result)
            if len(result):
                data = result.pop()
                return User(**data)

        else:
            user = self._token_memory[token]
            if user:
                user = json.loads(user)
                user = User(**user)
                user.token = token
                return user

        return None

    async def set(self, token, user: User):
        if tracardi.tokens_in_redis is False:
            record = {
                "doc": {"token": token},
                'doc_as_upsert': True
            }
            await self._elastic.update(self._index_write, user.email, record)
            await self._elastic.refresh(self._index_write)

        else:
            self._token_memory[token] = user.json()

    def update_user(self, user: User) -> None:
        if tracardi.tokens_in_redis is True:
            for key in self._token_memory.get_keys_by_email_hash(sha1(user.email.encode("utf-8")).hexdigest()):
                self._token_memory[key] = user.json()

    async def refresh_token(self, token) -> None:
        self._token_memory.refresh(token)


token2user = TokenDb()
