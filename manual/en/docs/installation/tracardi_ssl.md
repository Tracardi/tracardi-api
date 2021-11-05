# SSL Configuration

You have several options to run Tracardi in SSL mode.

## Building Tracardi with SSL certificates embedded into docker

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
COPY manual manual/
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

```
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 tracardi-api-ssl
```

## Running Tracardi with SSL certificates provided from outside container

Sometimes you do not want to build the docker yourself. Then you can use the prebuild docker and attach
value with your certificates. To do that pull `tracardi/tracardi-api-ssl`.

```
docker pull tracardi/tracardi-api-ssl
```

Then copy your SSL certificates to any folder. For the purpose of this manual we place it in `/local/path/to/ssl`.
You can place it anywhere but remember to change the location in the command below:

```
docker run \
-v /local/path/to/ssl:/ssl \
-p 8686:443 \
-e ELASTIC_HOST=http://<your-elastic-instance-ip>:9200 \
-e GUNICORN_CMD_ARGS="--keyfile=/ssl/key.pem --certfile=/ssl/cert.pem" \
tracardi/tracardi-api-ssl
```

It will start Tracardi with the provided certificates. This command expects na SSL key file to be named `key.pem` and
certificate to be named `cert.pem`.

## Tracardi behind HTTPS proxy

You can use treafic to hide Tracardi behind HTTPS proxy.

Refer to this link for instructions:
https://traefik.io/resources/traefik-fastapi-kuberrnetes-ai-ml/