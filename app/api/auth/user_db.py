import logging
from typing import Optional

from tracardi.config import tracardi
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage import index
from tracardi.service.storage.driver import storage
from tracardi.service.storage.elastic_client import ElasticClient

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class TokenDb:

    def __init__(self):
        self._elastic = ElasticClient.instance()
        self._index_write = index.resources['user'].get_write_index()

    async def delete(self, email):
        record = {
            "doc": {"token": None},
            'doc_as_upsert': True
        }
        await self._elastic.update(self._index_write, email, record)

    async def get(self, token) -> Optional[User]:

        # todo add caching

        logger.info(f"Reading user by token {token}")
        result = await storage.driver.user.search_by_token(token)

        if result.total > 1:
            raise ValueError(f"Invalid user count result. Expected 0 or 1 got {result.total}")

        result = list(result)
        if len(result):
            data = result.pop()
            return User(**data)

        return None

    async def set(self, email, token):
        record = {
            "doc": {"token": token},
            'doc_as_upsert': True
        }
        await self._elastic.update(self._index_write, email, record)
        await self._elastic.refresh(self._index_write)


token2user = TokenDb()
