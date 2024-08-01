# Building Docker Image

Sometimes you will need to build a docker container yourself. 
It is usually needed when you would like your docker server to run https requests. 

To build a docker container from source clone our repository

```
git clone https://github.com/tracardi/tracardi-api.git
```

Go to tracardi folder and run docker build

```
cd tracardi-api/
docker build . -t tracardi-api
```

After a while the docker will be built. It is on your computer, so you can run it like this.

```bash
docker run -p 8686:80 \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e MYSQL_HOST=<mysql-ip> \
tracardi/tracardi-api:<last-version> #(1)
```

1. Replace <...-ip> with your local laptop IP if the service is installed locally or with server IP where the service is installed. Replace <last-version> with the latest version. Do not use latest.


!!! Note "Replace <...-ip> with your laptop IP"

    Notice that that you can not type `http://localhost:9200`. This means that you're
    connecting to the docker itself as localhost means local in docker. Obviously elastic 
    is not there, so Tracardi will never connect. Pass external ip for elastic. 
    This may be your laptop IP if you are running Tracardi locally.

!!! Tip 
    
    On windows you can use `ipconfig` command to find out your laptop IP.
    
