docker build . --no-cache -f Dockerfile.ssl -t tracardi/tracardi-api-ssl
docker push tracardi/tracardi-api-ssl
docker build . --no-cache -f Dockerfile.ssl -t tracardi/tracardi-api-ssl:0.6.0
docker push tracardi/tracardi-api-ssl:0.6.0