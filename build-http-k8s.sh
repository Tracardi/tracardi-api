git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache --progress=plain -f docker.k8s.Dockerfile -t tracardi/tracardi-api-k8s:0.9.0-dev
#docker push tracardi/tracardi-api-k8s:0.9.0-dev