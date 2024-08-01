# Open-Source Installation

This guide will walk you through the process of installing Tracardi, which consists of four main components: API, GUI,
Automatic Profile Merging Worker (APM), and Update Worker.

## Docker compose installation

The simplest approach to installing Tracardi is by using Docker Compose. It's important to note that this installation
is intended for testing purposes only, as it doesn't configure all the required services properly.

1. **[Installation via docker compose](docker/docker_compose.md):** One liner installation for testing purposes.

## Docker one-by-one installation

The open-source version of Tracardi can be installed by starting each Docker container separately. You will need to
configure each Docker container to connect to the dependent services accordingly:

1. **[Docker one-by-one installation](docker/docker.md):** Description of all open-source Tracardi dockers.