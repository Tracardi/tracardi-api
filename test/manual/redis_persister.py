import asyncio

import msgpack
import random
import time
import redis

from com_tracardi.service.tracking.domain.hashable_dict_entity import HashableDictEntity
from com_tracardi.service.tracking.locking import GlobalMutexLock
from com_tracardi.service.tracking.storage_buffer import StorageBuffer
from tracardi.context import Context
from tracardi.domain.profile import Profile
from tracardi.service.storage.redis.collections import Collection


def _queue(context, data):
    print(context)
    print(len(data), data)


# Create a Redis connection
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
storage_buffer = StorageBuffer(pool_size=3, store_func=_queue, expire=120)


def get_prefixes():
    numbers = [format(num, '02x') for num in range(256)]
    random.shuffle(numbers)
    return numbers


async def yield_records(object_type):
    prefixes = get_prefixes()
    for collection_no, prefix in enumerate(prefixes):

        with GlobalMutexLock(prefix,
                             'redis:partition',
                             namespace=Collection.lock_persister,
                             redis=redis
                             ):

            # Pattern to match

            pattern = f"*:{object_type}:{prefix}:*"
            print(collection_no, pattern)
            # Initialize a cursor to start scanning
            cursor = 0

            # Collect keys matching the pattern without TTL set
            profile_keys = []

            # Use the SCAN command to iterate through keys matching the pattern

            while True:
                cursor, partial_keys = redis.scan(cursor, match=pattern)

                # Check if the cursor is 0, indicating that we've scanned all keys
                if cursor == 0:
                    break

                # Iterate over partial_keys
                for key in partial_keys:
                    key_name = key.decode('utf-8')
                    # Check if the key has a TTL set (-1 means no TTL)
                    value = redis.get(key_name)
                    if value is not None and redis.ttl(key_name) != -1:
                        # Decode value

                        value = msgpack.unpackb(value)

                        context, data, metadata = value
                        # Add the key to the profile_keys list
                        yield key_name, value
                        await storage_buffer.append(_context=Context(**context),
                                                    _data=HashableDictEntity({"entity": data}), _time_start=0)
                        redis.expire(key_name, 6000)


async def main():
    t = time.time()
    async for k in yield_records(object_type="profile"):
        print(len(k))
    print((time.time() - t))


asyncio.run(main())
