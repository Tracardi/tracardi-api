# Redis

!!! Notice

    It's important to note that this document does not cover the installation of Redis intended for production use. For information on setting up Redis for production environments, please refer to the official Redis documentation dedicated to production-ready installations.



Start standalone version of redis with:

```
docker run -p 6379:6379 redis
```

!!! Warning

    This docker does not have any storage volume attached to it so when stopped all the data will be lost. 

Please see the Apache Pulsar Documentation for proper installation.