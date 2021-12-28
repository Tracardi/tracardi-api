# Installation

The easiest way to run Tracardi is to run it as a docker container. 

In order to do that you must have docker installed on your local machine. 
Please refer to docker installation manual to see how to install docker.

## Dependencies

Tracardi need elasticsearch as its backend. Please pull and run elasticsearch 
single node docker before you start Tracardi. 

You can do it with this command.
```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

## Start Tracardi API

Now pull and run Tracardi backend.

```
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 -e USER_NAME=admin -e PASSWORD=admin tracardi/tracardi-api
```

Tracardi must connect to elastic. To do that you have to set ELASTIC_HOST variable 
to reference your laptop's or server IP.

Notice that when type `http://localhost:9200` you try to connect to Elastic on localhost. 
This means that you're connecting to the docker itself as localhost means local in docker. 
Obviously elastic is not there, so Tracardi will never connect. 
Pass external ip for elastic. This may be your laptop IP if you are running Tracardi locally. 

## Start Tracardi GUI

Now pull and run Tracardi Graphical User Interface.

```
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui
```

## Start Tracardi Documentation

Now pull and run Tracardi Documentation. This is the documentation you are reading right now 

```
docker run -p 8585:8585 tracardi/tracardi-docs
```

## Log-in

Visit http://127.0.0.1:8787 and login to Tracardi GUI.

Default username is: `admin`
Default password is: `admin`

To change the default login and password change the following environment variables:

* `USER_NAME` - Default: admin. Login to Tracardi API
* `PASSWORD` - Default: admin. Password to Tracardi API

See Tracardi configuration for details.

## System Documentation

Visit http://127.0.0.1:8585

## API Documentation

Visit http://127.0.0.1:8686/docs
