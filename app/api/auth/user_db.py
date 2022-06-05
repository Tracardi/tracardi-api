import logging
from typing import Optional

from tracardi.config import tracardi
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage import index
from tracardi.service.storage.driver import storage
from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.redis_client import RedisClient

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


class TokenDb:

    def __init__(self):
        if tracardi.tokens_in_redis is False:
            self._elastic = ElasticClient.instance()
            self._index_write = index.resources['user'].get_write_index()

        else:
            self._redis = RedisClient()

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
            self._redis.client.delete(f"AUTH-TOKEN-{token}")

    async def get(self, token) -> Optional[User]:

        # todo add caching

        logger.info(f"Reading user by token {token[:6]}...")

        if tracardi.tokens_in_redis is False:
            result = await storage.driver.user.search_by_token(token)
            if result.total > 1:
                raise ValueError(f"Invalid user count result. Expected 0 or 1 got {result.total}")

            result = list(result)
            if len(result):
                data = result.pop()
                return User(**data)

        else:
            email = self._redis.client.get(f"AUTH-TOKEN-{token}")
            result = await storage.driver.user.get_by_id(email)

            if result:
                return User(**result)

        return None

    async def set(self, email, token):
        if tracardi.tokens_in_redis is False:
            record = {
                "doc": {"token": token},
                'doc_as_upsert': True
            }
            await self._elastic.update(self._index_write, email, record)
            await self._elastic.refresh(self._index_write)

        else:
            self._redis.client.set(f"AUTH-TOKEN-{token}", email, ex=15*60)

    async def refresh_token(self, token) -> None:
        self._redis.client.expire(f"AUTH-TOKEN-{token}", 15*60)


token2user = TokenDb()
