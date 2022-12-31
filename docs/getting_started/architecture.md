# System architecture

Tracardi is a distributed system that consists of several components working together to track and analyze customer data. The core components of Tracardi include:

1. a database for storing events, a data processing library, 
2. a RESTful API and GraphQL API for interacting with the system, and 
3. a graphical user interface (GUI) for end users. 

Additionally, Tracardi includes background workers that perform background processes such as importing and segmentation.

## Components

**The data processing library** is a key component of Tracardi API that handles the workflow for selected events and transfers them to external systems. Programmers can use this library to develop Tracardi plugins. 

**The GUI** is a graphical interface that runs in the user's browser and allows end users to interact with the system.

**The background workers** that perform background processes such as merging and segmentation.

Tracardi components can be installed and run separately, and multiple instances of each component can be activated to meet the needs of the business. For the system to work fully, at least four elements must be activated: 

- the database, 
- the API, 
- the GUI, and 
- the background import worker. 

The GUI connects to the API, which in turn connects to the database.

In addition to the core components of Tracardi, the system may also include additional elements such as:
* background processes for profile merging and segmentation, 
* data bridges for connecting to external systems, 
* microservices, and more. 
