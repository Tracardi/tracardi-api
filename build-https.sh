docker build . --rm --no-cache -f docker.ssl.Dockerfile -t tracardi/tracardi-api-ssl:0.7.4
docker push tracardi/tracardi-api-ssl:0.7.4