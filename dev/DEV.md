# Run local server

PYTHONPATH=/home/risto/PycharmProjects/tracardi LOGGING_LEVEL=info POSTPONE_DESTINATION_SYNC=6 uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --workers 25
gunicorn -b 0.0.0.0:8686 -k uvicorn.workers.UvicornWorker app.main:application

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem  --ssl-keyfile-password 12345
gunicorn -b 0.0.0.0:443 --keyfile ssl/key.pem --certfile ssl/cert.pem -k uvicorn.workers.UvicornWorker app.main:application

# Run local Kibana
docker run -p 5601:5601 -m 4g -e ELASTICSEARCH_HOSTS=http://192.168.1.101:9200 docker.elastic.co/kibana/kibana:7.13.2

# Run local ElasticSearch
docker run -p 9200:9200 -p 9300:9300 -m 8g -e "discovery.type=single-node" -v "/opt/esdata:/usr/share/elasticsearch/data" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
docker run -p 9200:9200 -p 9300:9300 -m 8g -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

# Run local Tracardi GUI
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 -e TRACK_DEBUG="yes" tracardi/tracardi-gui

# Run local OpenSearch
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

# Run OpenDisto
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" amazon/opendistro-for-elasticsearch:latest

# Run local API
docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 -e RESET_PLUGINS=yes -e MAX_WORKERS=3 -e LOGGING_LEVEL=info tracardi/tracardi-api

# Run local redis
docker run -p 6379:6379 redis

# Run local jupyter notebook
docker run -p 8888:8888 jupyter/minimal-notebook

# Run local mysql
docker run -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -p 3306:3306 mysql
mysql -h localhost -P 3306 --protocol=tcp -u root -p root test
mysql -h localhost -P 3306 --protocol=tcp -u root -p 



# Run local mongo
docker run -p 27017:27017 mongo

# Run local PG
docker run -e POSTGRES_PASSWORD=root -p 5432:5432 postgres

# Run tracardi api with SSL

docker run -v /home/risto/PycharmProjects/tracardi-api/ssl:/ssl -p 8686:443 -e USER_NAME=admin -e PASSWORD=admin -e WORKERS=2 -e ELASTIC_HOST=http://192.168.1.103:9200 -e GUNICORN_CMD_ARGS="--keyfile=/ssl/key.pem --certfile=/ssl/cert.pem" tracardi/tracardi-api-ssl

# Run GUI HTTPS and HTTP
docker run -p 443:443 -p 80:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui-https


# Run Mkdocs
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material


docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 -e USER_NAME=admin -e PASSWORD=admin -e POSTPONE_DESTINATION_SYNC=6 -e LOGGING_LEVEL=info -e REDIS_HOST=redis://192.168.1.103:6379 tracardi/tracardi-api


# Generate certificate

openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

# Meatbeat
docker run docker.elastic.co/beats/metricbeat:7.13.4 setup -E setup.kibana.host=192.168.1.103:5601 -E output.elasticsearch.hosts=["192.168.1.103:9200"]

# Common Name must be localhost


# Celery worker
celery -A worker.celery_worker worker --loglevel=info -E
docker run -e REDIS_HOST=redis://redis-0.redis.redis.svc.cluster.local tracardi/worker
docker run -e REDIS_HOST=redis://192.168.1.101 tracardi/worker
