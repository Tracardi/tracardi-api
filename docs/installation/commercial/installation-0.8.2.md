# Commercial Installation

This guide gives you step-by-step instructions on how to install the commercial version of Tracardi for versions above
0.8.1. The system has been updated after version 0.8.1 to improve event collection performance and add new dependencies.
This installation process covers Tracardi 0.8.2 and later versions.

## Prerequisites

To set up Commercial Tracardi, you'll need access to DockerHub token and a valid commercial license key. This
information will be sent to you after purchase of the commercial license.

### Dependencies

Tracardi needs tha following systems:

* Database: Elasticsearch
* Cache: Redis
* Queue: Apache Pulsar

## Docker one-by-one installation

The installation of open-source version of Tracardi has the following steps:

1. **[API Installation](../docker/tracardi_com_with_docker.md#start-tracardi-api):** The API component serves as the
   interface through which various interactions with the Tracardi system.

2. **[GUI Installation](../docker/tracardi_com_with_docker.md#start-tracardi-gui):** The GUI (Graphical User Interface)
   is
   the visual representation of the Tracardi system.

3. **[Workers Installation](../workers/installation.md):** Workers are parts of the Tracardi
   system responsible for handling updates, segmentation, triggers, and maintenance tasks.

4. **[Jobs Installation](../jobs/index.md):** Jobs are parts of the Tracardi
   system responsible for triggering jobs for workers.

## Kubernetes' installation with helm

Soon to be released