docker compose -f dev-docker-compose.yaml up

# Run local server

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --workers 25 --log-level warning
PYTHONPATH=/home/risto/PycharmProjects/tracardi LOGGING_LEVEL=warning uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --workers 25 --log-level warning
gunicorn -b 0.0.0.0:8686 -k uvicorn.workers.UvicornWorker app.main:application

uvicorn app.main:application --reload --host 0.0.0.0 --port 8686 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem  --ssl-keyfile-password 12345
gunicorn -b 0.0.0.0:443 --keyfile ssl/key.pem --certfile ssl/cert.pem -k uvicorn.workers.UvicornWorker app.main:application

# Run local Kibana
docker run -p 5601:5601 -m 4g -e ELASTICSEARCH_HOSTS=http://192.168.1.110:9201 docker.elastic.co/kibana/kibana:7.13.2
docker run -p 5601:5601 -m 4g \
-e ELASTICSEARCH_HOSTS="https://192.168.1.110:9201" \
-e ELASTICSEARCH_USERNAME=elastic \
-e ELASTICSEARCH_PASSWORD=VwcljE20X3i05n64iPSP311z \
-e ELASTICSEARCH_SSL_VERIFICATIONMODE=none \
docker.elastic.co/kibana/kibana:7.13.2

# Run local ElasticSearch
docker run -p 9200:9200 -p 9300:9300 -m 8g -e "discovery.type=single-node" -v "/opt/esdata:/usr/share/elasticsearch/data" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
docker run -p 9200:9200 -p 9300:9300 -m 2g -e "discovery.type=single-node" -e ES_JAVA_OPTS="-Xms512m -Xmx512m" docker.elastic.co/elasticsearch/elasticsearch:7.13.2

# Run local redis
docker run -p 6379:6379 redis redis-server

# Run local mysql
docker run -e MYSQL_ROOT_PASSWORD=root  -p 3306:3306 mysql
mysql -h localhost -P 3306 --protocol=tcp -u root -p root test
mysql -h localhost -P 3306 --protocol=tcp -u root -p 

# Pulsar

docker run -it \
-p 6650:6650 \
-p 8080:8080 \
apachepulsar/pulsar:3.1.0 \
bin/pulsar standalone

# Starrock

docker run -p 9030:9030 -p 8030:8030 -p 8040:8040 -itd \
--name quickstart starrocks/allin1-ubuntu

# Run local Tracardi GUI
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 -e TRACK_DEBUG="yes" tracardi/tracardi-gui

# Run local API
docker run -p 18686:80 \
-e ELASTIC_HOST=http://192.168.1.110:9200 \
-e REDIS_HOST=redis://192.168.1.110:6379 \
-e MYSQL_HOST=192.168.1.110 \
-e PULSAR_HOST=pulsar://192.168.1.110:6650 \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-api:0.9.0-rc3

# Rabbit mq

docker run -p 15672:15672 -p 5672:5672 --hostname my-rabbit-2 --name some-rabbit-2 rabbitmq:3-management



# Run Mkdocs
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material


docker run -p 8686:80 -e ELASTIC_HOST=http://192.168.1.103:9200 -e USER_NAME=admin -e PASSWORD=admin -e LOGGING_LEVEL=info -e REDIS_HOST=redis://192.168.1.103:6379 tracardi/tracardi-api

# minio
docker run -p 9000:9000 -p 9001:9001 -e "MINIO_ROOT_USER=admin" -e "MINIO_ROOT_PASSWORD=admin" minio/minio server /data --console-address :9001

# keycloak - https://inteca.com/identity-access-management/keycloak-docker-a-comprehensive-guide-to-deploying-and-managing-your-identity-and-access-management-solution/
# http://localhost:8080/auth/admin
docker run -p 8080:8080 -e KEYCLOAK_USER=admin -e KEYCLOAK_PASSWORD=admin jboss/keycloak


# Generate certificate

openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out cert.pem

# Kafka UI

docker run -p 8080:8080 \
	-e KAFKA_CLUSTERS_0_NAME=local \
	-e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092 \
	-d provectuslabs/kafka-ui:latest


# Kafka

docker run --rm --net=host landoop/fast-data-dev
