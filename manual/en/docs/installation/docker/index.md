# Docker container installation

The easiest way to run Tracardi is to run it as a docker container.

## Start database

Tracardi need elasticsearch as its backend. Please pull and run elasticsearch single node docker before you start
Tracardi.

You can do it with this command.

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

!!! Note

    Running one instance of elasticsaerch is not a production solution. For production purposes, 
    it is necessary to run the elasticearch cluster. You can also [read here how to connect Tracardi](../../configuration/elasticsearch/connecting_elasticsearch_cluster.md) 
    to an elasticsearch cluster

#### Redis

If you use features as destinations, import, or synchronized events then you will need a redis instance as well.

Start it with:

```
docker run -p 6379:6379 redis
```

## Start Tracardi API

!!! Note

    The following instalation description use the latest tracardi container version. If you would like to install stable version 
    of the system, what we strongly recommend, please add to `tracard/tracardi-api` a tag with version, e.g `tracardi/tracardi-api:0.7.0`. 
    The same applies to `tracardi/tracardi-gui`. Keep the version of API and GUI the same. 

### Run Tracardi API

Now pull and run Tracardi backend.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 -e REDIS_HOST=redis://<your-laptop-ip>:6379 tracardi/tracardi-api #(1)
```

1. Replace <your-laptop-ip> with your local laptop IP. You can remove `-e REDIS_HOST=redis://<your-laptop-ip>:6379` if
   you did not start redis. Without redis some system features are unavailable.

Tracardi must connect to elasticsearch. To do that you have to set ELASTIC_HOST variable to reference your laptop's or
server IP.

!!! Warning "Waiting for application startup"

    Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic is not there, so Tracardi will
    never connect. Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally.

For more trouble shooting solutions go to [Troubleshooting](../../trouble/index.md)


### Connecting Tracardi to ElasticSearch via SSL

If you have an elasticsearch instance and you would like to connect to it via HTTPS this is the command you may find
useful.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=https://user:password@<your-laptop-ip>:9200 -e ELASTIC_VERIFY_CERTS=no -e REDIS_HOST=redis://<your-laptop-ip>:6379 tracardi/tracardi-api #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-api:0.7.0`

!!! Warning "ELASTIC_VERIFY_CERTS set to No"

    Notice that the above command does not verify SSL certificates. If you would like certificates to be validated set 
    ELASTIC_VERIFY_CERTS to yes.

## Start Tracardi GUI

Pull and run Tracardi Graphical User Interface.

```bash
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-gui:0.7.0`

!!! Note

    Notice that the `API_URL` is set to `localhost`. If the API is located somewhere else __replace localhost with the
    ip pointing to API__.

## Import worker

To run an import worker you will need the tracari/worker to do the background importing of the data. Run the following 
command to start the worker. 

```bash
docker run -e REDIS_HOST=redis://<redis-ip>:6379 -d tracardi/worker #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/worker:0.7.0`


!!! Note

    Replace the `<redis-ip>` with the IP of the redis instance. Keep the version of worker the same as 
    `tracard/tracardi-api`

## Start Tracardi Documentation

Pull and run Tracardi Documentation. This is the documentation you are reading right now

```bash
docker run -p 8585:8585 tracardi/tracardi-docs
```

## Tracardi Graphical User Interface

Visit http://127.0.0.1:8787 and follow the instructions to set-up Tracardi.

## System Documentation

For the local copy of this documentation visit http://127.0.0.1:8585. The documentation docker must be started. 

## API Documentation

For API documentation visit http://127.0.0.1:8686/docs
