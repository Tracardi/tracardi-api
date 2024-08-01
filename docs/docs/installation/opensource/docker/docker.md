# Docker-based Tracardi Open-Source Installation

!!! Notice

    Make sure you have docker installed on your system.

!!! Notice

    The following instalation description use the latest tracardi container version. If you would like to install stable version 
    of the system, what we strongly recommend, please add to `tracard/tracardi-api` a tag with version, e.g `tracardi/tracardi-api:0.8.1`. 
    The same applies to `tracardi/tracardi-gui`. Keep the version of API, GUI, and APM the same. 

## Start Tracardi API

Pull and run Tracardi backend.

```bash
docker run -p 8686:80 \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
tracardi/tracardi-api:<last-version> #(1)
```

1. Replace <...-ip> with your local laptop IP if the service is installed locally or with server IP where the service is installed. Replace <last-version> with the latest version. Do not use latest.

Tracardi must connect to dependant services. To do that you have to set ELASTIC_HOST, REDIS_HOST, MYSQL_HOST variable to reference your laptop's or
server IP.

!!! Warning "Please use the version tag"

    Please use only docker with version tag. Do not use latest. See the version in docker hub. 


!!! Warning "Waiting for application startup"

    Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic is not there, so Tracardi will
    never connect. Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally.

### API Documentation

For API documentation visit http://127.0.0.1:8686/docs

## Start Tracardi GUI

Pull and run Tracardi Graphical User Interface.

```bash
docker run -p 8787:80 tracardi/tracardi-gui:<last-version> #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-gui:0.8.1`

!!! Warning "Please use the version tag"

    Please use only docker with version tag. See the latest version in docker hub. 

## Run Tracardi Graphical User Interface

Visit http://127.0.0.1:8787 and follow the instructions to finish up the Tracardi set-up. 
When asked for Tracardi API type: http://127.0.0.1:8686. 


## Start Tracardi APM (Automatic Profile Merging)

Pull and run Tracardi APM.

```bash
docker run \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
-e MODE=worker \
-e PAUSE=5 \
tracardi/apm:<last-version>
```