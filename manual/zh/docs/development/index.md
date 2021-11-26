# Tracardi GUI

To start working on Tracardi GUI clone tracardi-gui repo.

```
git clone http://github.com/tracardi/tracardi-gui
```

Then run:

```
yarn install
```

This will install all project dependencies.

## Starting GUI

In the project directory, you run:

### `yarn start`

This will run the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you edit  source code. \
You will also see any lint errors in the console.

# Tracardi API

To start working on Tracardi API clone tracardi-api repo.

Once cloned run:

```
cd tracardi-api
pip install -r api/requirements.txt
uvicorn app.main:application --reload --host 0.0.0.0 --port 8686
```

This will start tracardi API on port 8686

# Tracardi Database

You need elasticsearch for Tracardi to work.

Run a single node elastic in docker:

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```