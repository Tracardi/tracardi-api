# Commercial Installation

This guide will provide step-by-step instructions for installing commercial Tracardi. Some aspects of this installation
process are quite similar to the open-source installation.

## Prerequisites

To set up Commercial Tracardi, you'll need access to DockerHub token and a valid commercial license key. This information will
be sent to you after the purchase of the commercial license.

## Docker compose installation

The simplest approach to installing Tracardi is by using Docker Compose. It's important to note that this installation
is intended for testing purposes only, as it doesn't configure and scale the dependant services properly.

1. **[Installation via docker compose](docker/docker_compose.md):** One liner installation for testing purposes.

## Kubernetes' installation with helm

1. **[Installation with Helm on K8S](helm/index.md):** Automates installation of all required Tracardi components.

