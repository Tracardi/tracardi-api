import base64

import msgpack

from tracardi.context import ServerContext, Context
from tracardi.service.adapter.cache.redis.redis_cache_adapter import RedisCacheAdapter
from tracardi.service.adapter.cache.upstash.upstash_redis_cache_adapter import UpStashRedisCacheAdapter

v = msgpack.packb(("xxx"))
encoded_string = base64.b64encode(v).decode('utf-8')
print(type(encoded_string))

with ServerContext(Context(production=False)):
    redis = UpStashRedisCacheAdapter()
    redis = RedisCacheAdapter()

    v = (1,2,3)
    print(v)
    print(redis.set_msgpack("8504a", v , ex=1800))
    value = redis.get_msgpack("8504a")
    print(type(value), value)

