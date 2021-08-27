# Run local server

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686
gunicorn -b 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker app.main:application

uvicorn app.main:application --reload --host 0.0.0.0 --port 8001 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem  --ssl-keyfile-password 12345
gunicorn -b 0.0.0.0:433 --keyfile ssl/key.pem --certfile ssl/cert.pem -k uvicorn.workers.UvicornWorker app.main:application

# Run local kibana
docker run --name kibana --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://localhost:9200" docker.elastic.co/kibana/kibana:7.13.3

# Run local elastic
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

# Run local API
docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 tracardi/tracardi-api:0.6.0