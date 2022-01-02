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

## Start Tracardi API

Pull and run Tracardi backend.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 -e USER_NAME=admin -e PASSWORD=admin tracardi/tracardi-api  #(1)
```

1. Replace <your-laptop-ip> with your local laptop IP

Tracardi must connect to elasticsearch. To do that you have to set ELASTIC_HOST variable to reference your laptop's or server
IP.

!!! Warning "Waiting for application startup"

    Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic is not there, so Tracardi will
    never connect. Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally.

## Start Tracardi GUI

Pull and run Tracardi Graphical User Interface.

```bash
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui
```

## Start Tracardi Documentation

Pull and run Tracardi Documentation. This is the documentation you are reading right now

```bash
docker run -p 8585:8585 tracardi/tracardi-docs
```

## Tracardi Graphical User Interface

Visit http://127.0.0.1:8787 and login to Tracardi GUI.

Default username is: `admin`
Default password is: `admin`

To change the default login and password change the following environment variables:

* `USER_NAME` - Default: admin. Login to Tracardi API
* `PASSWORD` - Default: admin. Password to Tracardi API

See Tracardi configuration for details.

## System Documentation

Visit http://127.0.0.1:8585

## API Documentation

Visit http://127.0.0.1:8686/docs
