# Commercial Tracardi with docker compose

This guide provides a brief introduction on how to install and test the commercial version of Tracardi using
docker-compose. Please note that this installation is not intended for production use, but rather for testing purposes
only.

In order to install commercial version you will need to log-in to docker hub with our credentials.

```
docker login -u tracardi -p <token>
```

And paste the credentials that we have sent you.

## Set up License Key

Then create a file .env-docker and paste the LICENSE in it:

```
API_LICENSE="paste license here"
```

When running linux:

```
set -a
source .env-docker
```

## Clone Tracardi API

```bash
git clone https://github.com/Tracardi/tracardi-api.git
```

## Run docker compose

Go to TRACARDI API folder, and run one line command:

```bash
cd tracardi-api
docker-compose -f com-docker-compose.yaml up
```

!!! Note

    To run docker compose in the background add `-d` to the command above.

!!! Warning

    Tracardi, to operate with its full range of features, requires the presence of specific crontab jobs. 
    It's important to note that when using Docker Compose, these crontab jobs are not automatically included as 
    part of the setup. Therefore, to ensure that Tracardi functions as intended, it is essential to perform an 
    additional crontab installation.

## Upgrading docker compose

1. **Stopping Docker Compose**

   Prior to upgrading, ensure that your Docker Compose configuration is not running. Execute the following command in your terminal:

   ```bash
   docker compose down
   ```

2. **Pulling New Images**

   To upgrade to the latest version, fetch the latest Docker images for the components. Run the following commands in your terminal:

   ```bash
   docker pull tracardi/tracardi-api:0.8.1
   docker pull tracardi/tracardi-gui:0.8.1
   docker pull tracardi/update-worker:0.8.1
   docker pull tracardi/com-tracardi-segmentation-worker:0.8.1
   docker pull tracardi/com-tracardi-scheduler-worker:0.8.1
   docker pull tracardi/com-tracardi-coping-worker:0.8.1
   docker pull tracardi/com-tracardi-trigger-worker:0.8.1
   ```

## Handling Errors

If you encounter errors while bringing up the upgraded Docker Compose setup, it might be necessary to address these
errors by deleting certain components. Follow the steps below:

- To stop all running containers (make sure that there are no other container running but the tracardi containers),
  execute:

  ```bash
  docker kill $(docker ps -q)
  ```

- To delete unused containers, volumes, images, and networks, run:

  ```bash
  docker container prune
  docker volume prune
  docker image prune
  docker network prune
  ```
   