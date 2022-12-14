docker build . --rm --no-cache -f docker.ssl.Dockerfile -t tracardi/tracardi-api-ssl:0.8.0-dev
docker push tracardi/tracardi-api-ssl:0.8.0-dev