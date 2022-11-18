pip install -r requirements.dev.txt
# Uncomment in version branch. DO not use in master branch
#docker build . --rm --no-cache -f Dockerfile.ssl -t tracardi/tracardi-api-ssl
#docker push tracardi/tracardi-api-ssl