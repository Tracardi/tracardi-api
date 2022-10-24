git rev-parse HEAD > app/tracker/revision.txt
docker build . -f Dockerfile.k8s -t tracardi/tracardi-api-k8s:0.7.2.1
docker push tracardi/tracardi-api-k8s:0.7.2.1