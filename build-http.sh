git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -f docker.Dockerfile -t tracardi/tracardi-api:2.0.x-dev
docker push tracardi/tracardi-api:2.0.x-dev