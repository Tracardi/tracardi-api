from time import sleep

from tracardi.context import ServerContext, Context
from tracardi.service.storage.redis.cache import RedisCache


def test_redis_cache():
    value = {
            "a": {
                "b": [1, 2, 3]
            },
            "c": {
                "d": None
            }
        }
    collection = "pytest:"
    rc = RedisCache(ttl=1)

    if not rc.has("key", collection):
        assert rc.get("key", collection) is None
    else:
        rc.delete("key", collection)

    rc.set("key", value, collection)

    assert rc.get("key", collection) == value

    # Can be deleted

    rc.delete("key", collection)

    rc.delete("key", collection)
    assert rc.get("key", collection) is None

    # Expires

    rc.set("key", value, collection)

    sleep(2)

    assert rc.get("key", collection) is None

