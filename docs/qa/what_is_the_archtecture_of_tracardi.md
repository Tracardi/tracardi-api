# What is the architecture of Tracardi?

Tracardi is a distributed system that consists of several components working together to track and analyze customer
data. The core components of Tracardi include:

- an ElasticSearch database for storing events,
- a Redis server for caching,
- a RESTful API,
- a graphical user interface (GUI) for end-users.

Additionally, Tracardi includes background workers that perform background processes such as importing and segmentation.

## Communication

The GUI connects to the API, which in turn connects to the database. Tracardi components can be installed and run
separately, and multiple replicas of each component can be activated to meet the needs of the business.

For the system to work fully, at least four elements must be activated, including the database, API, GUI, and the
background import worker. The architecture allows for additional elements such as microservices, data bridges and
background processes for profile merging and segmentation.