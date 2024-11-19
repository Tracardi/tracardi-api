docker build . --rm --no-cache -f docker.ssl.Dockerfile -t tracardi/tracardi-api-ssl:1.2.x
docker push tracardi/tracardi-api-ssl:1.2.x