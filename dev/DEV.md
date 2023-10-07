# Run local server

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --workers 25 --log-level warning
PYTHONPATH=/home/risto/PycharmProjects/tracardi LOGGING_LEVEL=warning uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --workers 25 --log-level warning
gunicorn -b 0.0.0.0:8686 -k uvicorn.workers.UvicornWorker app.main:application

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem  --ssl-keyfile-password 12345
gunicorn -b 0.0.0.0:443 --keyfile ssl/key.pem --certfile ssl/cert.pem -k uvicorn.workers.UvicornWorker app.main:application

# Run local Kibana
docker run -p 5601:5601 -m 4g -e ELASTICSEARCH_HOSTS=http://192.168.1.107:9200 docker.elastic.co/kibana/kibana:7.13.2

# Run local ElasticSearch
docker run -p 9200:9200 -p 9300:9300 -m 8g -e "discovery.type=single-node" -v "/opt/esdata:/usr/share/elasticsearch/data" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
docker run -p 9200:9200 -p 9300:9300 -m 2g -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms512m -Xmx512m" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

# Run local redis
docker run -p 6379:6379 redis redis-server --notify-keyspace-events Ex


# Run local Tracardi GUI
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 -e TRACK_DEBUG="yes" tracardi/tracardi-gui

# Run local OpenSearch
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" opensearchproject/opensearch:latest

# Run OpenDisto
docker run -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" amazon/opendistro-for-elasticsearch:latest

# Run local API
docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 -e LOGGING_LEVEL=info tracardi/tracardi-api

# Rabbit mq

docker run -p 15672:15672 -p 5672:5672 --hostname my-rabbit-2 --name some-rabbit-2 rabbitmq:3-management


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

# Run clickhouse
docker run -d -p 18123:8123 -p19000:9000 --ulimit nofile=262144:262144 clickhouse/clickhouse-server


# Run tracardi api with SSL

docker run -v /home/risto/PycharmProjects/tracardi-api/ssl:/ssl -p 8686:443 -e USER_NAME=admin -e PASSWORD=admin -e WORKERS=2 -e ELASTIC_HOST=http://192.168.1.103:9200 -e GUNICORN_CMD_ARGS="--keyfile=/ssl/key.pem --certfile=/ssl/cert.pem" tracardi/tracardi-api-ssl
docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.106:9200 -e tracardi/tracardi-api:0.8.2-dev


# Run GUI HTTPS and HTTP
docker run -p 443:443 -p 80:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui-https


# Run Mkdocs
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material


docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 -e USER_NAME=admin -e PASSWORD=admin -e LOGGING_LEVEL=info -e REDIS_HOST=redis://192.168.1.103:6379 tracardi/tracardi-api

# minio
docker run -p 9000:9000 -p 9001:9001 -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=admin" minio/minio server /data --console-address :9001


# Generate certificate

openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

# Meatbeat
docker run docker.elastic.co/beats/metricbeat:7.13.4 setup -E setup.kibana.host=192.168.1.103:5601 -E output.elasticsearch.hosts=["192.168.1.103:9200"]

# Common Name must be localhost


# Celery worker
celery -A worker.celery_worker worker --loglevel=info -E
docker run -e REDIS_HOST=redis://redis-0.redis.redis.svc.cluster.local tracardi/worker
docker run -e REDIS_HOST=redis://192.168.1.101 tracardi/worker


# Kafka UI

docker run -p 8080:8080 \
	-e KAFKA_CLUSTERS_0_NAME=local \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092 \
	-d provectuslabs/kafka-ui:latest


# Kafka

docker run --rm --net=host landoop/fast-data-dev


# Matomo

helm upgrade matomo --set service.ports.http=9080,service.ports.https=9443,externalDatabase.host=192.168.1.190,externalDatabase.user=root,externalDatabase.password=root bitnami/matomo


# Pulsar

docker run -it \
-p 6650:6650 \
-p 8080:8080 \
apachepulsar/pulsar:3.1.0 \
bin/pulsar standalone


# ISSUES:
 Can't logi in:
 
delete the user index and reinstall


curl -k -X DELETE "https://elastic:0q2673s1zLAZ9IPi22CEBlq2@localhost:9200/080.fa73a.tracardi-user?pretty"