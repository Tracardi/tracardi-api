pip install -r requirements.dev.txt
# Uncomment in version branch. DO not use in master branch
git rev-parse HEAD > app/tracker/revision.txt
docker build . --rm --no-cache -t tracardi/tracardi-api
docker push tracardi/tracardi-api
