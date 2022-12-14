git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -f docker.Dockerfile -t tracardi/tracardi-api:0.7.4
docker push tracardi/tracardi-api:0.7.4
