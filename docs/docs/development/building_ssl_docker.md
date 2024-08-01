# Build SSL Docker

## Building Tracardi API with SSL certificates embedded into docker

Clone repository `tracardi/tracardi-api.git`.

```
git clone https://github.com/tracardi/tracardi-api.git
```

Next go to tracardi folder and find file **Dockerfile.ssl-internal** and type path to your SSL certificate and key file. 

* Find and replace `ssl/key.pem` with a path to your key file
* Find and replace `ssl/cert.pem` with a path to your certificate

This is how the **Dockerfile.ssl-internal** looks like

```
FROM tiangolo/uvicorn-gunicorn-fastapi

RUN apt-get update
RUN apt-get install -y git

# set the working directory in the container
RUN mkdir app/
WORKDIR /app

## Install dependencies
COPY app/requirements.txt .
RUN pip install -r requirements.txt

## Copy application
COPY app app/
COPY ssl ssl/
COPY docs manual/
ENV VARIABLE_NAME="application"

EXPOSE 443
CMD ["gunicorn", "-b", "0.0.0.0:443", "--workers", "25,"--keyfile", "ssl/key.pem", "--certfile", "ssl/cert.pem", "-k", "uvicorn.workers.UvicornWorker", "app.main:application"]
```

If you would like to tweak the number of workers running change `--workers` option in `gunicorn`.

Then run

```
cd tracardi-api/
docker build . -f Dockerfile.ssl-internal -t tracardi-api-ssl
```

Once built you can run Tracardi with the following command:

```bash title="Run docker and open port 8686"
docker run -p 8686:443 \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
tracardi/tracardi-api-ssl:<last-version> #(1)
```

1. Replace <...-ip> with your local laptop IP if the service is installed locally or with server IP where the service is installed. Replace <last-version> with the latest version. Do not use latest.


This will make API available at __https://localhost:8686__. If you want it on the standard HTTPS port run:

```bash title="Run docker and open port 443"
docker run -p 443:443 \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
tracardi/tracardi-api-ssl:<last-version> #(1)
```

1. Replace <...-ip> with your local laptop IP if the service is installed locally or with server IP where the service is installed. Replace <last-version> with the latest version. Do not use latest.


And the API will be available __https://localhost__.