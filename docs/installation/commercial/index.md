# Installation of commercial version

This guide provides a brief introduction on how to install and test the commercial version of Tracardi using
docker-compose. Please note that this installation is not intended for production use, but rather for testing purposes
only.

In order to install commercial version you will need to login to docker hub with our credentials.

```
docker login
```

And paste the credentials that we have sent you.

Then create a file .env-docker and paste the LICENSE in it:

```
API_LICENSE="paste license here"
```

When running linux:

```
set -a
source .env-docker
```

Then run the com-docker-compose.yaml as docker compose file.

```
docker-compose -f com-docker-compose.yaml up
```