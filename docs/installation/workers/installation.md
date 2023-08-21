# Workers Installation

Tracardi relies on four different workers to ensure smooth operations and efficient processing of data. Each worker
serves a specific purpose in the Tracardi ecosystem. Below are details about each worker and instructions on how to set
them up.

## Open-source workers

### 1. Migration and Import Worker

The Migration and Import Worker is responsible for system upgrades and data import tasks, which are carried out in the
background. It ensures a seamless transition when updating the Tracardi system and handles data imports efficiently.

To run the Migration and Import Worker, execute the following Docker command:

```bash
docker run \
-e REDIS_HOST=redis://<redis-ip>:6379 \
tracardi/update-worker:0.8.1
```

Please ensure that you replace `<redis-ip>` with the actual IP address of your Redis instance.

## Commercial workers

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

### 2. Segmentation and Mapping

The Commercial Worker for Segmentation, Post-Collection Event Mapping, and Post-Collection Profile Mapping plays a vital
role in processing commercial tasks, including segmentation (both workflow and conditional) and mapping events and
profiles after collection.

To run this worker, execute the following Docker command:

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-segmentation-worker:0.8.1
```

### 3. Scheduler Worker

The Scheduler Worker is a commercial worker responsible for processing delayed events. It ensures that time-based
triggers and other delayed tasks are executed efficiently.

To run the Scheduler Worker, execute the following Docker command:

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=<redis-ip> \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-scheduler-worker:0.8.1
```

### 4. Post-Collection Worker

The Post-Collection Event Mapping, and Post-Collection Profile Mapping is required for mapping events and
profiles after collection.

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-coping-worker:0.8.1
```

### 5. Trigger Worker

The trigger worker is in charge of initiating workflows when a profile gets added to a specific segment.

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e LOGGING_LEVEL=info \
tracardi/com-tracardi-trigger-worker:0.8.1
```
