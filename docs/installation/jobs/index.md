# Tracardi Jobs

Tracardi utilizes jobs that can be initiated through Kubernetes (k8s) or set up as cronjobs. These jobs play crucial
roles in the commercial Tracardi platform. The following jobs need to be started:

1. **Heartbeat Job**: This job is responsible for closing sessions, marking profiles and sessions as inactive.
   Heartbeats are periodic checks that identify certain patterns indicating inactivity. For example, if a session is not
   closed, meaning there is no "session closed" event registered after a specific period of time from the last recorded
   event, it indicates that the customer has left the page.

2. **Segmentation Job**: This job executes segmentations on profiles based on predefined time intervals, such as hourly.
   Workflow segmentations and conditional segmentations rely on this job. It requires the Segmentation Worker to be
   running, as the job initiates the segmentation task, which is then completed by the Segmentation Worker.

## Job Docker Containers

### Heartbeat Job

To run the Heartbeat Job, use the following Docker command for the `tracardi/com-heartbeat-job` container:

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e REDIS_PASSWORD=password \
-e PRODUCTION=yes \
-e RANGE=now-1h|now \
-e SKIP_SECONDS=900 \
-e QUALIFY_BY=inactive-session \
-e EVENT_TYPE=session-inactive \
tracardi/com-heartbeat-job:0.8.1
```

Description of environment variables:

- `PRODUCTION`: Specifies whether the job should run on production data.
- `RANGE`: Determines the number of records to fetch and search for the defined event types. It corresponds to the time
  interval that the job runs. For example, if it runs every 1 hour, the time range should be larger than 1 hour.
- `SKIP_SECONDS`: Represents the allowed time of inactivity after the last registered event for a profile.
- `QUALIFY_BY`: Specifies the qualifying operation or pattern to match. In this case, "inactive-session" indicates that
  the job searches for inactive sessions.
- `EVENT_TYPE`: Defines the event type that must be registered if it qualifies for it.

Each job serves a specific purpose, and the provided example focuses on the Heartbeat Job, which looks for sessions
without a `session-inactive` event within the time range of now and -1 hour. If there is no `session-inactive` event,
the job registers a "Session Inactive" event in the system.

Other values for `QUALIFY_BY` include:

- `inactive-profile`: Searches for inactive profiles, allowing users to define the time range and event type to trigger.
- `inactive-session`: Looks for inactive sessions, indicating no events within the defined time frame.
- `session-not-closed`: Searches for sessions that were not closed after a period of customer inactivity.


#### Examples

Here are the example Docker commands that you could run in cronjob:

1. Session Inactive Job (SCHEDULE="*/8 * * * *"):

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e REDIS_PASSWORD=password \
-e RANGE="now-1h|now" \
-e QUALIFY_BY="inactive-session" \
-e SKIP_SECONDS=900 \
-e EVENT_TYPE="session-inactive" \
tracardi/com-heartbeat-job:0.8.1
```

2. Session Close Job (SCHEDULE="*/15 * * * *"):

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e REDIS_PASSWORD=password \
-e RANGE="now-1h|now" \
-e QUALIFY_BY="session-not-closed" \
-e SKIP_SECONDS=1800 \
-e EVENT_TYPE="session-closed" \
tracardi/com-heartbeat-job:0.8.1
```

3. Inactive Profile Job (SCHEDULE="13 4 1 * *"):

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e REDIS_PASSWORD=password \
-e RANGE="now-1y|now" \
-e QUALIFY_BY="inactive-profile" \
-e SKIP_SECONDS=15548736 \
tracardi/com-heartbeat-job:0.8.1
```

Ensure that you replace `<elastic-ip>` and `<redis-ip>` with the actual IP addresses for your ElasticSearch and Redis instances, respectively. Also, make sure to provide the correct image version (`0.8.1`) based on your Tracardi setup.

Jobs can be scheduled and run using crontab or Kubernetes cron jobs based on your preferred deployment method.

### Segmentation Job

To run the Segmentation Job, use the following Docker command for the `tracardi/com-tracardi-segmentation-worker`
container:

```bash
docker run \
-e ELASTIC_HOST=http://<elastic-ip>:9200 \
-e REDIS_HOST=redis://<redis-ip>:6379 \
-e REDIS_PASSWORD=password \
tracardi/com-tracardi-segmentation-worker:0.8.1
```

The Segmentation Job uses the same environment variables as `tracardi/tracardi-api`. Ensure that all the connections are
configured correctly.

