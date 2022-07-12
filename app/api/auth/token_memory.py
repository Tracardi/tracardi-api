from tracardi.service.storage.redis_client import RedisClient


class TokenMemory:

    def __init__(self):
        self._redis = RedisClient()
        self.ttl = 30 * 60

    def __setitem__(self, key, value):
        self._redis.client.set(f"AUTH-TOKEN-{key}", value, ex=self.ttl)

    def __getitem__(self, key):
        return self._redis.client.get(f"AUTH-TOKEN-{key}")

    def __delitem__(self, key):
        self._redis.client.delete(f"AUTH-TOKEN-{key}")

    def refresh(self, key):
        self._redis.client.expire(f"AUTH-TOKEN-{key}", self.ttl)

    def get_keys_by_email_hash(self, email_hash):
        for key in self._redis.client.keys(f"AUTH-TOKEN-{email_hash}-*"):
            yield key
