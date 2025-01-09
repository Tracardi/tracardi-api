#git rev-parse HEAD > app/tracker/revision.txt
docker build . --progress=plain --build-arg GITHUB_TOKEN=${GITHUB_TOKEN}  -f docker.Dockerfile -t tracardi/tracardi-api:1.3.x-alpha1
#docker push tracardi/tracardi-api:1.3.x-alpha1