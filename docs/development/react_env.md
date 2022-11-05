# ReactJs development environment

## Software prerequisites

* Docker
* Node
* Yarn
* VSCode or WebStorm
* Git

To start working on Tracardi GUI clone tracardi-gui repo.

```bash
git clone http://github.com/tracardi/tracardi-gui  #(1)
```

1. Clones GUI source code from GitHub

Then run:

```bash
yarn install  #(1)
```

1. This will install all project dependencies.

## Starting GUI

In the project directory, run:

```bash
yarn start
```

This will run the app in the development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the
browser. The page will reload if you edit source code. You will also see any lint errors in the console.

!!! Info In order to work with GUI you will need Tracardi API. Below you will find instructions how to run API with
docker.

## Dependencies

Tracardi GUI depends on 1 service: Tracardi-API, but API depends on another 2 services which are: elasticsearch and redis.

### Tracardi Database

You need elasticsearch for Tracardi to work.

Run a single node elastic in docker:

```bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

### Redis

You will need a redis instance as well.

Start it with:

```
docker run -p 6379:6379 redis
```

## Tracardi API

To start Tracardi API pull and run Tracardi API docker image.

```bash
docker run -p 8686:80 -e ELASTIC_HOST=http://<elasticsearch-IP>:9200 -e REDIS_HOST=redis://<redis-IP>:6379 tracardi/tracardi-api
```

Replace `<elasticsearch-IP>` and `<redis-IP>` with your laptop ip. You can obtain it in windows by typing command line `ipconfig`. 

This will start tracardi API on port 8686

## More information

If you encounter some issues when starting the API please go to [installation guide](../installation/docker/index.md)
for more information.
