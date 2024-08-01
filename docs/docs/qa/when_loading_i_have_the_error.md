# When loading I Have the error `Redis Authentication`?

This error is related to the connection to Redis. It indicates that Tracardi was unable to log in to the Redis server.

# When loading I Have the error `Redis authentication error: AUTH <password> called without any password configured for the default user. Are you sure your configuration is correct?`?

The Tracardi application is configured to use a Redis password, but the Redis server does not require a password. As a result, Tracardi is sending a password to Redis, but Redis is not using it.