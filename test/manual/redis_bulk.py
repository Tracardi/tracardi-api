import time

import redis

# Create a Redis connection
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Define the pattern to match
pattern = "01506:profile:*"

# Initialize a cursor to start scanning
cursor = 0

# Collect keys matching the pattern without TTL set
profile_keys = []

# Use the SCAN command to iterate through keys matching the pattern
t = time.time()
while True:
    cursor, partial_keys = r.scan(cursor, match=pattern)

    # Check if the cursor is 0, indicating that we've scanned all keys
    if cursor == 0:
        break

    # Iterate over partial_keys
    for key in partial_keys:
        key_name = key.decode('utf-8')
        # Check if the key has a TTL set (-1 means no TTL)
        if r.ttl(key_name) != -1:
            # Add the key to the profile_keys list
            profile_keys.append(key_name)
            r.expire(key_name, 600)
print((time.time() - t) /4000)
# Print the keys and their TTLs (optional)
# for key_name in profile_keys:
#     ttl = r.ttl(key_name)
#     print(f"Key: {key_name}, TTL: {ttl} seconds")