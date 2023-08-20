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