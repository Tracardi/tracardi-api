docker build . --rm --no-cache -f docker.ssl.Dockerfile -t tracardi/tracardi-api-ssl:1.0.x-dev
docker push tracardi/tracardi-api-ssl:1.0.x-dev