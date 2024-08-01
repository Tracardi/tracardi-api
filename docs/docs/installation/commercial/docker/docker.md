# Docker-based Tracardi Commercial Installation

!!! Note

    Make sure you have docker installed on your system.

!!! Note

    The following instalation description use the latest tracardi container version. If you would like to install stable version 
    of the system, what we strongly recommend, please add to `tracard/com-tracardi-api` a tag with version, e.g `tracardi/com-tracardi-api:0.8.1`. 
    The same applies to `tracardi/tracardi-gui`. Keep the version of API and GUI the same. 

## Prerequisites

### Access to commercial dockers

When you buy a Tracardi license, you'll get a DockerHub token. This token lets you download the commercial dockers.

Tracardi GUI looks the same in both the open-source and commercial versions. The only difference is the Tracardi API.

```bash title="Login to Docker Hub"
docker login -u tracari -p <token>
```

Then create a file .env-docker and paste the LICENSE in it:

```bash title="Set the LICENSE"
API_LICENSE="paste license here"
```

When running linux:

``` title="Set the LICENSE"
set -a
source .env-docker
```

## Init script

Before you run any commercial docker please make sure that all dependencies are running and you start init script. This script will initialize all required databases, etc.:

```bash title="docker run command to setup tracardi environment"
docker run \
-e LICENSE=xxx \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
-e PULSAR_HOST=pulsar://<pulsar-ip>:6650 \
-e PULSAR_API=http://<pulsar-ip>:8080 \
-e LOGGING_LEVEL=info \
tracardi/init:<last-version>
```

Please ensure that you replace `<...-ip>` with the actual IP address of your service instance.

## Tracardi API

Pull and run Tracardi backend.

```bash
docker run -p 8686:80 \
-e LICENSE=xxx \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
-e PULSAR_HOST=pulsar://<pulsar-ip>:6650 \
-e PULSAR_API=http://<pulsar-ip>:8080 \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-api:<last-version> #(1)
```

1. Replace `<elastic-ip>` with your elastic IP. Do the same for `<redis-ip>`, `<mysq-ip>`, and `<pulsar-ip>`. Replace <
   last-version> with the latest version. Do not use latest.

Tracardi must connect to elasticsearch. To do that you have to set ELASTIC_HOST variable to reference your elasticsearch
instance.

!!! Warning "Please use the version tag"

    Please use only docker with version tag. Do not use latest tag. See the the version in docker hub. 

!!! Warning "Waiting for application startup"

    Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic is not there, so Tracardi will
    never connect. Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally.

### Test installation

To test API visit http://127.0.0.1:8686

## Tracardi GUI

Pull and run Tracardi Graphical User Interface.

```bash
docker run -p 8787:80 tracardi/tracardi-gui:<last-version> #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/tracardi-gui:0.8.1`

!!! Warning "Please use the version tag"

    Please use only docker with version tag. See the latest version in docker hub. 

### Run Tracardi GUI

Visit http://127.0.0.1:8787 and follow the instructions to finish up the Tracardi set-up. When asked for Tracardi API
type: http://127.0.0.1:8686.

## Tracardi Workers Installation

Tracardi relies on four different workers to ensure smooth operations and efficient processing of data. Each worker
serves a specific purpose in the Tracardi ecosystem. Below are details about each worker and instructions on how to set
them up.

### Open-source workers

#### 1. Migration and Update Worker

The Migration and Update Worker is responsible for system upgrades and data import tasks, which are carried out in the
background. It ensures a seamless transition when updating the Tracardi system and handles data imports efficiently.

To run the Migration and Update Worker, execute the following Docker command:

```bash title="docker run command"
docker run \
-e ELASTIC_HOST=http://<elasitc-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
tracardi/update-worker:<last-version>
```

Please ensure that you replace `<...-ip>` with the actual IP address of your service instance.

#### 2. Automatic Profile Merging Worker (APM)

The APM Worker is responsible for auto merging profiles with the same emails.

To run the APM Worker, execute the following Docker command:

```bash title="docker run command"
docker run \
-e ELASTIC_HOST=http://<elasitc-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
-e MODE=worker \
-e PAUSE=5 \
tracardi/apm:<last-version>
```

Please ensure that you replace `<...-ip>` with the actual IP address of your service instance.

### Commercial workers

In order to install commercial version you will need to log-in to docker hub with our credentials.

```
docker login -u tracardi -p <token>
```

And paste the credentials that we have sent you.



#### 1. Tenant Management System (TMS)

The Tenant Management System (TMS) is a dedicated microservice responsible for managing various aspects related to
tenants within a system or platform, particularly in a multi-tenant environment. I

To run this worker, execute the following Docker command:

```bash title="docker run command"
docker run -p 8081:80 \
-e API_KEY=<random-api-key> \
-e SECRET=<random-secret> \
-e MYSQL_HOST=<mysql-ip> \
tracardi/tms:<last-version>
```

Set <random-api-key> and <random-secret> to random values.

#### 2. Background Worker

The Background Worker is a commercial worker responsible for processing background jobs.

To run the Background Worker, execute the following Docker command:

```bash title="docker run command"
docker run \
-e LICENSE=xxx \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
-e PULSAR_HOST=pulsar://<pulsar-ip>:6650 \
-e PULSAR_API=http://<pulsar-ip>:8080 \
-e LOGGING_LEVEL=info \
tracardi/background-worker:<last-version>
```

Please ensure that you replace `<...-ip>` with the actual IP address of your service instance.