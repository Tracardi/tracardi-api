git rev-parse HEAD > app/tracker/revision.txt
docker build . --no-cache -t tracardi/tracardi-api
docker push tracardi/tracardi-api
