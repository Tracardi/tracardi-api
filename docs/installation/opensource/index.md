# Open-Source Installation

Welcome to the installation documentation for the open-source version of Tracardi. This guide will walk you through the
process of installing Tracardi, which consists of three main components: API, GUI, and Update Worker.

## Docker compose installation

The simplest approach to installing Tracardi is by using Docker Compose. It's important to note that this installation
is intended for testing purposes only, as it doesn't configure the database and Redis properly.

1. **[Installation via docker compose](../docker-compose/opensource.md):** One liner installation for testing purposes.

## Docker one-by-one installation

The installation of open-source version of Tracardi has the following steps:

1. **[API Installation](../docker/tracardi_with_docker.md#start-tracardi-api):** The API component serves as the
   interface through which various interactions with the Tracardi system.

2. **[GUI Installation](../docker/tracardi_with_docker.md#start-tracardi-gui):** The GUI (Graphical User Interface) is
   the visual representation of the Tracardi system.

3. **[Update Worker Installation](../workers/install_update_worker.md):** The Update Worker is a part of the Tracardi
   system responsible for handling updates, patches, and maintenance tasks.

