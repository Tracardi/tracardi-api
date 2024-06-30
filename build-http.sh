git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -f docker.Dockerfile -t tracardi/tracardi-api:1.0.0
docker push tracardi/tracardi-api:1.0.0