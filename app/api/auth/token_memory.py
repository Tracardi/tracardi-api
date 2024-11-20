from tracardi.service.adapter.cache.cache_protocol import CacheProtocol
from tracardi.service.adapter.cache_adaper_selector import cache_adapter
from tracardi.service.singleton import Singleton
from tracardi.service.storage.redis.collections import Collection
from tracardi.config import tracardi
from hashlib import sha1


class TokenMemory(metaclass=Singleton):

    def __init__(self):
        self._cache: CacheProtocol = cache_adapter()
        self.ttl = 30 * 60
        instance_hash = sha1(f"{tracardi.version.version}.{tracardi.version.name}".encode("utf-8")).hexdigest()
        self.instance_hash = f"{Collection.token}{instance_hash}"

    def __setitem__(self, token, value):
        self._cache.set(f"{self.instance_hash}-{token}", value, ex=self.ttl)

    def __getitem__(self, token):
        return self._cache.get(f"{self.instance_hash}-{token}")

    def __delitem__(self, token):
        self._cache.delete(f"{self.instance_hash}-{token}")

    def refresh(self, token):
        self._cache.expire(f"{self.instance_hash}-{token}", self.ttl)
