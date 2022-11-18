pip install -r requirements.dev.txt
git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -t tracardi/tracardi-api:0.7.3
docker push tracardi/tracardi-api:0.7.3
