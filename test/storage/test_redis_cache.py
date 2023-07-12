from time import sleep

from tracardi.context import ServerContext, Context
from tracardi.service.storage.redis.cache import RedisCache


def test_redis_cache():
    with ServerContext(Context(production=False)):
        value = {
            "a": {
                "b": [1, 2, 3]
            },
            "c": {
                "d": None
            }
        }
        rc = RedisCache(ttl=1, prefix="pytest:")

        if "key" not in rc:
            assert rc["key"] is None
        else:
            del rc["key"]

        rc["key"] = value

        assert rc["key"] == value

        # Can be deleted

        del rc['Not-exists']

        del rc["key"]
        assert rc["key"] is None

        # Expires

        rc["key"] = value

        sleep(2)

        assert rc["key"] is None
