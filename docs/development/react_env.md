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

1. Clones GUI source code from github

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

This will run the app in the development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.
The page will reload if you edit source code. You will also see any lint errors in the console.

# Tracardi API

To start Tracardi API pull and run Tracardi Graphical User Interface docker image.

```bash
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui
```

This will start tracardi API on port 8686

# Tracardi Database

You need elasticsearch for Tracardi to work.

Run a single node elastic in docker:

```bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```