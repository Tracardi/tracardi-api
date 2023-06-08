# Why does the Tracardi API connection with Elasticsearch fail when using "localhost" as the ELASTIC_HOST?

When running Tracardi API within docker container with "localhost" as the ELASTIC_HOST, it means that the connection is
being made within the Docker container itself. However, Elasticsearch is not present within the Docker container,
leading to connection failure. To resolve this, it is necessary to provide the external IP address of the Elasticsearch
server, such as the laptop's IP address when running Tracardi locally.