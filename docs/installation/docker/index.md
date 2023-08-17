# Docker container installation

Utilizing a Docker container for Tracardi is the most straightforward method. For testing purposes, the default
installation mode of Tracardi is Docker-based.

## Dependencies

For Tracardi to function, you need these essential components:

- Elasticsearch
- Redis

Start the Docker containers for all the mentioned services.

## Dependency Installation

Refer to [this page](../dependencies/index.md) for instructions on installing dependencies, Elasticsearch, and Redis
using Docker.

## Tracardi API and GUI

Minimal Tracardi Docker installation involves GUI and API setup. For a installation guide, refer
to [this page](tracardi_with_docker.md).

## Additional services

Some Tracardi features need extra services to work.

### Import worker

To run an import worker you will need the tracardi/update-worker to do the background importing of the data. Run the
following command to start the worker.

```bash
docker run -e REDIS_HOST=redis://<redis-ip>:6379 -d tracardi/update-worker:0.8.0 #(1)
```

1. If you want a certain version of docker image add version tag, e.g. `tracardi/worker:0.8.0`

!!! Note

    Replace the `<redis-ip>` with the IP of the redis instance. Keep the version of worker the same as 
    `tracard/tracardi-api`





