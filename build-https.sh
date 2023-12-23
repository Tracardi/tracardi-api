docker build . --rm --no-cache -f docker.ssl.Dockerfile -t tracardi/tracardi-api-ssl:0.9.0-dev
docker push tracardi/tracardi-api-ssl:0.9.0-dev