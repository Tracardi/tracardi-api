# Tracardi Worker Installation

Tracardi relies on three different workers to ensure smooth operations and efficient processing of data. Each worker
serves a specific purpose in the Tracardi ecosystem. Below are details about each worker and instructions on how to set
them up.

## 1. Migration and Import Worker

The Migration and Import Worker is responsible for system upgrades and data import tasks, which are carried out in the
background. It ensures a seamless transition when updating the Tracardi system and handles data imports efficiently.

To run the Migration and Import Worker, execute the following Docker command:

```bash
docker run \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e ELASTIC_VERIFY_CERTS=no \
-e ELASTIC_HOST=http://<elasticsearch-ip>:9200 \
tracardi/worker:0.8.1
```

Please ensure that you replace `<redis-ip>` with the actual IP address of your Redis instance, the same goes
for `<elasticsearch-ip>`. The environment variables required for this worker are the same as those used for
the `tracardi/tracardi-api` Docker container.

## 2. Commercial Worker for Segmentation and Mapping

The Commercial Worker for Segmentation, Post-Collection Event Mapping, and Post-Collection Profile Mapping plays a vital
role in processing commercial tasks, including segmentation (both workflow and conditional) and mapping events and
profiles after collection.

To run this worker, execute the following Docker command:

```bash
docker run \
-e ELASTIC_HOST=http://192.168.1.101:9200 \
-e REDIS_HOST=redis://192.168.1.101:6379 \
tracardi/com-tracardi-segmentation-worker:0.8.1
```

## 3. Scheduler Worker

The Scheduler Worker is a commercial worker responsible for processing delayed events. It ensures that time-based
triggers and other delayed tasks are executed efficiently.

To run the Scheduler Worker, execute the following Docker command:

```bash
docker run \
-e ELASTIC_HOST=http://192.168.1.101:9200 \
-e REDIS_HOST=192.168.1.101 \
tracardi/com-tracardi-scheduler-worker:0.8.1
```

## Additional Information

For more detailed information on the features and capabilities of the Scheduler Worker, please refer to the
documentation pages that cover its functionalities. These pages will provide you with insights into effectively
utilizing the Scheduler Worker to meet your specific use cases and requirements.