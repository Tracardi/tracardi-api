# Pulsar docker installation

Start standalone version of Apache Pulsar with:

```
docker run -it \
-p 6650:6650 \
-p 8080:8080 \
apachepulsar/pulsar:3.1.0 \
bin/pulsar standalone
```

This docker does not have any storage volume attached to it so when stopped all the data will be lost. 