git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache --progress=plain -f docker.k8s.Dockerfile -t tracardi/tracardi-api-k8s:1.2.x
#docker push tracardi/tracardi-api-k8s:1.2.x