# Installing Tracardi Dependencies

This guide explains how to install the database and cache for Tracardi. Note that this setup is not suitable for
production use. For a production-ready setup, consult the Elasticsearch and Redis documentation. This is intended for
testing purposes only.

## Start ElasticSearch database

Tracardi need elasticsearch as its backend. Please pull and run elasticsearch single node docker before you start
Tracardi.

You can do it with this command.

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

!!! Warning

    The provided docker command lacks a persistent volume, which means that when you stop the Docker container, 
    all the data will be lost. If you wish to preserve the data between Docker container restarts, you can use the 
    following command: `docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -v /path/on/host:/usr/share/elasticsearch/data docker.elastic.co/elasticsearch/elasticsearch:7.13.2`. 
    To ensure data persistence, replace /path/on/host in the command with the directory path on your computer 
    where you would like to store the Elasticsearch data.

!!! Note

    Running one instance of elasticsaerch is not a production solution. For production purposes, 
    it is necessary to run the elasticearch cluster. You can also [read here how to connect Tracardi](../../configuration/elasticsearch/connecting_elasticsearch_cluster.md) 
    to an elasticsearch cluster

## Redis

You will need a redis instance as well.

Start it with:

```
docker run -p 6379:6379 redis
```