# Installing Dependencies

This guide explains how to install the necessary services for Tracardi to run properly. Please note that this setup is
intended for testing purposes only and is not suitable for production use. For a production-ready setup, please refer to
the Elasticsearch and Redis documentation.


!!! Notice

    Open source Tracardi requires only: Redis, ElasticSearch, and MySql to run. Prerequisites for Commercial Tracardi are installed clusters of: Redis, ElasticSearch, MySql, and Apache Pulsar.

## Dependencies installation

We have several options when installing dependencies. Use your preferred method.

### Docker installation

* [Elasticsearch docker installation](docker/elasticsearch.md) - version up to 8.11.3 
* [Redis docker installation](docker/redis.md) - Tracardi should work with any version of Redis. Recently tested version (7.2.4)
* [Apache Pulsar docker installation](docker/pulsar.md) - version 3.1.0
* [Mysql docker installation](docker/mysql.md) - version 8.3. Tracardi also works on percona version tested on 8.0.36.

### Installation from DEB

* [Elasticsearch DEB installation](deb/elasticsearch.md)

### Installation from Helm Chart

The preferred method for installing commercial Tracardi dependencies is through Helmchart. To use this method, you will
need access to commercial scripts that automate the installation process.

* [Elasticsearch K8S Helm Chart installation](helm/elasticsearch.md)
* [Redis K8S Helm Chart  installation](helm/redis.md)
* [Apache Pulsar doK8S Helm Chart cker installation](helm/pulsar.md)
* [Mysql K8S Helm Chart  installation](helm/mysql.md)