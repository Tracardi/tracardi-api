[![header.jpg](https://raw.githubusercontent.com/atompie/tracardi/tracardi-unomi-master/screenshots/github-splash.png)](https://raw.githubusercontent.com/atompie/tracardi/tracardi-unomi-master/screenshots/github-splash.png)

# Tracardi Open-source Customer Data Platform

Tracardi is an open-source Customer Data Platform.

TRACARDI is an API-first solution, low-code / no-code platform aimed at any e-commerce business that 
wants to start using user data for marketing purposes. If you own a brand-new e-commerce platform or 
a legacy system you can integrate TRACARDI easily. Use TRACARDI for:

 * **Customer Data Integration** - You can ingest, aggregate and store customer data
   from multiple sources in real time at any scale and speed due to elastic search backend.
   
 * **Customer Data Modelling** -  You can manage data. Define rules that will model data delivered
   from your page and copy it into user profile. You can segment customers into custom segments.
   
 * **User Experience Personalization** - You can personalize user experience with
   real-time customer segmentation and targeting.
   
 * **Profile Unification** - You can merge customer data from various sources to
   single profile. Auto de-duplicate customer records. Blend customers in one account.
   
 * **Automation** - TRACARDI is a great framework for creating
   marketing automation apps. You can send your data to other systems easily

## Screenshots

![Screenshot 1](https://raw.githubusercontent.com/atompie/tracardi/0.5.0-dev/raw/intro5.png)

Please see [https://github.com/tracardi/tracardi](https://github.com/tracardi/tracardi) for installation instructions.

# Installation

The easiest way to run Tracardi is to run it as a docker container. 

In order to do that you must have docker installed on your local machine. 
Please refer to docker installation manual to see how to install docker.

## Dependencies

Tracardi need elasticsearch as its backend. Please pull and run elasticsearch single node docker before you start Tracardi. 

You can do it with this command.
```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.2
```

## Start Tracardi API

Now pull and run Tracardi backend.

```
docker run -p 8686:80 -e ELASTIC_HOST=http://<your-laptop-ip>:9200 -e USER_NAME=admin -e PASSWORD=admin tracardi/tracardi-api
```

Tracardi must connect to elastic. To do that you have to set ELASTIC_HOST variable to reference your laptop's IP. 

## Start Tracardi GUI

Now pull and run Tracardi Graphical User Interface.

```
docker run -p 8787:80 -e API_URL=//127.0.0.1:8686 tracardi/tracardi-gui
```

## Start Tracardi Documentation

Now pull and run Tracardi Documentation.

```
docker run -p 8585:8585 tracardi/tracardi-docs
```

## Log-in

Visit http://127.0.0.1:8787 and login to Tracardi GUI with default username: admin and password: admin. 

## System Documentation

Visit http://127.0.0.1:8585

## API Documentation

Visit http://127.0.0.1:8686/docs

# License

Tracardi is available under MIT with Common Clause license.

