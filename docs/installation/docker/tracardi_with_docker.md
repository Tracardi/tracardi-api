# Docker-based Tracardi Installation

Make sure you have docker installed on your system.

## Tracardi API Version

!!! Note

    The following instalation description use the latest tracardi container version. If you would like to install stable version 
    of the system, what we strongly recommend, please add to `tracard/tracardi-api` a tag with version, e.g `tracardi/tracardi-api:0.8.1`. 
    The same applies to `tracardi/tracardi-gui`. Keep the version of API and GUI the same. 

### Start Tracardi API

Pull and run Tracardi backend.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 -e REDIS_HOST=redis://<your-laptop-ip>:6379 tracardi/tracardi-api #(1)
```

1. Replace <your-laptop-ip> with your local laptop IP. 

Tracardi must connect to elasticsearch. To do that you have to set ELASTIC_HOST variable to reference your laptop's or
server IP.

!!! Warning "Waiting for application startup"

    Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic is not there, so Tracardi will
    never connect. Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally.

For more troubleshooting solutions go to [Troubleshooting](../../trouble/index.md)

!!! More

    For more elasticseach connection types, e.g. via HTTP see [advanced elasticsearch connection](../../configuration/elasticsearch/elastic_https.md).

### API Documentation

For API documentation visit http://127.0.0.1:8686/docs

## Start Tracardi GUI

Pull and run Tracardi Graphical User Interface.

```bash
docker run -p 8787:80 tracardi/tracardi-gui #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-gui:0.8.1`

## Run Tracardi Graphical User Interface

Visit http://127.0.0.1:8787 and follow the instructions to finish up the Tracardi set-up. 
When asked for Tracardi API type: http://127.0.0.1:8686. 