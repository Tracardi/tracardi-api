docker build . --no-cache -t tracardi/tracardi-api
docker push tracardi/tracardi-api
docker build . --no-cache -t tracardi/tracardi-api:0.6.0
docker push tracardi/tracardi-api:0.6.0
