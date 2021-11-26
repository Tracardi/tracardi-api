## Building Tracardi docker from source

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

After a while the docker will be build. It is on your computer, so you can run it like this.

```
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 tracardi-api
```
