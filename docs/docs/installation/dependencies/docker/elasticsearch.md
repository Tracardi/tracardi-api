# Elasticsearch

!!! Notice

    It's important to note that this document does not cover the installation of Elasticsearch intended for production use. For information on setting up Elasticsearch for production environments, please refer to the official Elasticsearch documentation dedicated to production-ready installations.

## ElasticSearch database as docker

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
    it is necessary to run the elasticearch cluster. Last tested version that is compatible with tracardi is: 8.11.3. 
    We suggest installing version 7.13.2 as this version we use for our internal testing.  

---
Questions answered by this document:

* What are the software prerequisites for installation from source?
* How do you configure Elasticsearch?
* How do you install Elasticsearch as a docker container?