git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm -f docker.k8s.Dockerfile -t tracardi/tracardi-api-k8s:0.7.4-dev
docker push tracardi/tracardi-api-k8s:0.7.4-dev