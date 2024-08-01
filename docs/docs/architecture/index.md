# Architecture of Tracardi

Tracardi uses Docker as a containerization platform. For production installation, we recommend using Kubernetes to
manage Tracardi Docker instances securely and efficiently.

The Tracardi stack requires an operating system capable of hosting a Kubernetes (K8s) cluster. On top of this,
Kubernetes and all Tracardi dependencies need to be installed. These dependencies include Elasticsearch, MySQL, Redis,
and Apache Pulsar, which can be hosted either within the Kubernetes cluster or externally. Scaling Tracardi effectively
relies on the scaling of these dependencies.

Tracardi is a distributed system designed to track and analyze customer data. It consists of several core components:

1. **Database**: Stores events and other data.
2. **API**: A RESTful interface for interacting with the system.
3. **GUI**: A graphical user interface for end users.
4. **Background Workers**: Handle background processes such as profile merging and tenant management.

## Components

- **Data Processing Library**: This key component of the Tracardi API handles workflow for selected events and transfers
  them to external systems. Programmers can use this library to develop Tracardi plugins.
- **GUI**: A graphical interface that runs in the user's browser, allowing end users to interact with the system.
- **Background Workers**: Perform background processes such as merging profiles and managing tenants.

Tracardi components can be installed and run separately, and multiple instances of each component can be activated to
meet business needs. For the system to function fully, at least four elements must be activated:

- Database
- API
- GUI
- Background Workers

The GUI connects to the API, which in turn connects to the database.

In addition to the core components, Tracardi may also include additional elements such as:

- Background processes for profile merging
- Data bridges for connecting to external systems
- Multitenancy controllers

These auxiliary services enhance Tracardi's functionality.

## Open-Source vs Commercial

The commercial version of Tracardi requires more services than the open-source one. Unlike the open-source version, the
commercial version relies on Apache Pulsar and includes additional features such as multitenancy controllers, new data
collection bridges, and enhanced profile management workers. In contrast, the open-source version does not depend on
Apache Pulsar and features an extended API, offering a different set of capabilities tailored to commercial use cases.