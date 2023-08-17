# Connecting Tracardi to ElasticSearch via SSL

If you have an elasticsearch instance and you would like to connect to it via HTTPS this is the command you may find
useful.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=https://user:password@<your-laptop-ip>:9200 -e ELASTIC_VERIFY_CERTS=no -e REDIS_HOST=redis://<your-laptop-ip>:6379 tracardi/tracardi-api #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-api:0.8.1`

!!! Warning "ELASTIC_VERIFY_CERTS set to No"

    Notice that the above command does not verify SSL certificates. If you would like certificates to be validated set 
    ELASTIC_VERIFY_CERTS to yes.