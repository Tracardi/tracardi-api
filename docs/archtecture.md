# Technology Overview: Prerequisites, Design, and Platform Requirements

## Design

Tracardi is structured as a microservices-based platform, functioning as a distributed system with fault tolerance by
operating as stateless pods.

## Prerequisites

### Underlying Infrastructure

Tracardi is specifically designed to operate within a Kubernetes cluster, making a Kubernetes cluster a fundamental
requirement. This Kubernetes environment serves not only as a host for Tracardi but also as a platform for deploying and
managing the essential dependent technologies, including Redis, Elasticsearch, and Apache Pulsar. All of these
technologies can be conveniently integrated within the Kubernetes ecosystem.

### Dependencies

- Elasticsearch as underlying storage
- Redis as intermediate cache
- Apache Pulsar as event queue

#### Dependency Configuration

The resource allocation for Redis, Elasticsearch, and Apache Pulsar should be tailored to the scale of data collected.
This means that the customer has the flexibility to determine the number of nodes and their configurations according to
their specific needs. Tracardi is versatile enough to operate even within standalone instances of Redis, Elasticsearch,
and Apache Pulsar, without the need for clustering.

It is considered a best practice to deploy each dependent system in a fault-tolerant manner, ensuring that the failure
of one component does not disrupt the overall system.

### Technologies in Use

Tracardi employs a diverse set of technologies for its components:

- Tracardi uses Docker as its containerization platform for packaging and deploying its microservices and components.
- Tracardi's API is implemented in Python and operates on an asynchronous FastAPI REST server.
- The Tracardi GUI is developed using ReactJS.
- Tracardi's worker processes are predominantly coded in Python and subscribe to Apache Pulsar topics for efficient data
  processing.
- For task scheduling, Tracardi leverages Kubernetes CronJobs.
- Apache Pulsar is the backbone of Tracardi's data queue management.
- Redis is used for in-memory profile data storage.

### Scalability

Tracardi's scalability is realized by replicating its API and worker instances. The initial resource requirements for
the API Event Collector are modest, necessitating only 0.1 CPU and 100MB of RAM. However, it can be scaled up to handle
increased loads, with an upper limit of 0.5 CPU and 250MB of RAM. It is important to note that the API Event Collector
operates as an asynchronous, single-threaded micro application.

### Workers

Tracardi employs a collection of microservices known as workers to execute various background tasks. The following is a
list of available workers, and it is possible to expand this list based on specific installation requirements:

- Flusher Workers: These workers are responsible for persisting data changes to Apache Pulsar topics.
- Storage Workers: Their primary function is to store and manage data.
- Computation Workers: These workers handle tasks related to profile metrics, segmentation, and other data processing
  tasks.

### Networking

Tracardi offers two API configurations: an external API with a restricted set of endpoints and a comprehensive external
API providing access to all available endpoints for system management. To enhance security, it is highly recommended to
segregate the internal and external APIs in a way that prevents direct internet access to the internal API, thereby
strengthening the system's defense against potential external threats.