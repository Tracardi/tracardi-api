# Run local server

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686
gunicorn -b 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker app.main:application

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem  --ssl-keyfile-password 12345
gunicorn -b 0.0.0.0:433 --keyfile ssl/key.pem --certfile ssl/cert.pem -k uvicorn.workers.UvicornWorker app.main:application

# Run local Kibana
docker run -p 5601:5601 -e ELASTICSEARCH_HOSTS=http://192.168.1.103:9200 docker.elastic.co/kibana/kibana:7.13.2

# Run local ElasticSearch
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

# Run local OpenSearch
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

# Run OpenDisto
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" amazon/opendistro-for-elasticsearch:latest

# Run local API
docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 tracardi/tracardi-api

# Run local redis
docker run -p 6379:6379 redis

# Run local jupyter notebook
docker run -p 8888:8888 jupyter/minimal-notebook

# Run local mysql
docker run -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -p 3306:3306 mysql
mysql -h localhost -P 3306 --protocol=tcp -u root -p root test


# Run local mongo
docker run -p 27017:27017 mongo

# Run local PG
docker run -e POSTGRES_PASSWORD=root -p 5432:5432 postgres

# Run tracardi api with SSL

docker run -v /home/risto/PycharmProjects/tracardi-api/ssl:/ssl -p 8686:433 -e ELASTIC_HOST=http://192.168.1.103:9200 -e GUNICORN_CMD_ARGS="--keyfile=/ssl/key.pem --certfile=/ssl/cert.pem" tracardi/tracardi-api-ssl

