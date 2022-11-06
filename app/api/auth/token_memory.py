from tracardi.service.singleton import Singleton
from tracardi.service.storage.redis_client import RedisClient
from tracardi.config import tracardi
from hashlib import sha1


class TokenMemory(metaclass=Singleton):

    def __init__(self):
        self._redis = RedisClient()
        self.ttl = 30 * 60
        self.instance_hash = sha1(f"{tracardi.version.version}.{tracardi.version.name}".encode("utf-8")).hexdigest()

    def __setitem__(self, token, value):
        self._redis.client.set(f"{self.instance_hash}-{token}", value, ex=self.ttl)

    def __getitem__(self, token):
        return self._redis.client.get(f"{self.instance_hash}-{token}")

    def __delitem__(self, token):
        self._redis.client.delete(f"{self.instance_hash}-{token}")

    def refresh(self, token):
        self._redis.client.expire(f"{self.instance_hash}-{token}", self.ttl)

