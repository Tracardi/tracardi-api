git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -f docker.Dockerfile -t tracardi/tracardi-api:0.8.0
docker push tracardi/tracardi-api:0.8.0
