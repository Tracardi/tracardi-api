from tracardi.service.storage.redis_client import RedisClient
from tracardi.config import elastic
from hashlib import sha1


class TokenMemory:

    def __init__(self):
        self._redis = RedisClient()
        self.ttl = 30 * 60
        self._elastic_identifier = sha1(f"{elastic.host}".encode("utf-8")).hexdigest()

    def __setitem__(self, key, value):
        self._redis.client.set(f"AUTH-TOKEN-{self._elastic_identifier}-{key}", value, ex=self.ttl)

    def __getitem__(self, key):
        return self._redis.client.get(f"AUTH-TOKEN-{self._elastic_identifier}-{key}")

    def __delitem__(self, key):
        self._redis.client.delete(f"AUTH-TOKEN-{self._elastic_identifier}-{key}")

    def refresh(self, key):
        self._redis.client.expire(f"AUTH-TOKEN-{self._elastic_identifier}-{key}", self.ttl)
