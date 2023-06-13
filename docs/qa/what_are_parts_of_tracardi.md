# What are the main components or modules that make up Tracardi?

Tracardi consist of the following docker images. 

!!! Note

    Docker image name is given in the brackets.

## Backend

- Database: Elasticsearch (docker.elastic.co/elasticsearch/elasticsearch)

- Redis: Cache (redis)

- Open-source Tracardi API (tracardi/tracardi-api)

- Open-source Tracardi Workers (tracardi/tracardi-api)
  - Various Import Workers
  - Migration Worker
  
- Commercial Tracardi API (tracardi/com-tracardi-api)
  - Tenant Manager API
  
- Commercial Tracardi brides (tracardi/com-bridge-queue)
  - MQTT,
  - Kafka
  - IMAP
  - RabbitMq
  
- Commercial REST Bridge + Worker (tracardi/com-bridge-rest-worker, tracardi/com-bridge-rest)

- Commercial Workers
  - Scheduler (tracardi/com-tracardi-scheduler + tracardi/com-tracardi-scheduler-worker)
  
- Commercial Jobs
  - Heartbeat (tracardi/com-heartbeat-job)
  - Session closer
  - Segmentation (tracardi/com-tracardi-segmentation-job + tracardi/com-tracardi-segmentation-worker)
  
- Sponsored GraphQl (tracardi/com-graphql)

- Tracardi PRO

- Misc (most obsolete):
  - Deduplication (tracardi/com-job-deduplication)
  - Merging (tracardi/com-job-merging)
  - Segmentation (tracardi/com-job-segmentation)


## Frontend

- Tracardi Graphical User Interface

## Optional
- 
- Kibana as analytical tool

## Programming

- Tracardi Library (http://www.github.com/tracardi/tracardi)

---
This document also answers the questions.

- Provide an overview of the different components that comprise Tracardi?
- What are the key building blocks or modules that constitute Tracardi?
- Break down the various parts or elements that make up Tracardi?
- What are the fundamental components or sections within Tracardi?
- What are the primary constituent parts or components?
- What are the main sections or building elements that constitute Tracardi?
