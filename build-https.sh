pip install -r requirements.dev.txt
docker build . --rm --no-cache -f Dockerfile.ssl -t tracardi/tracardi-api-ssl:0.7.3
docker push tracardi/tracardi-api-ssl:0.7.3