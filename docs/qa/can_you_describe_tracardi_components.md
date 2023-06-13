# Can you describe Tracardi components?

This is technical documentation of source code and dockers.

## Commercial Tracardi API

- Source: com-tracardi/com_tracardi, tracardi/tracardi
- Github: https://github.com/Tracardi/com-tracardi, https://github.com/Tracardi/tracardi
- Docker: tracardi/com-tracardi-api
- Description: This is commercial Tracardi API responsible for collecting and processing events.

## Commercial Jobs

### Heartbeats

- Source: com-tracardi/com_job/heartbeat
- Github: https://github.com/Tracardi/com-tracardi
- Docker: tracardi/com-heartbeat-job
- Description: This job is responsible for running some defined event on all profiles. It has defined strategies such
  as:
    - inactive-profile: Gets profiles if no event happened in `wait_period` time and there was no event
      type `event_type` E.g. This allows to raise for example an event `inactive` if no activity on profile in 2 days
      and no `inactive` event available in all profile events.
    - inactive-session:  Gets session if no event happened in `wait_period` time and there was no event
      type `event_type`. E.g. This allows to raise for example an event `inactive` if no activity in 15 min and
      no `inactive` event available within the session
    - session-not-closed: Gets all profiles if there is no event for a defined period (15 min) and raise session closed
      event.

### Live Segmentation

- Source: com-tracardi/com_job/segmentation
- Github: https://github.com/Tracardi/com-tracardi
- Docker: tracardi/com-tracardi-segmentation-job
- Description: Iterate over live segmentation flows and push to the segmentation:live queue a job for worker that
  segments the profile based on the live workflows.

## Commercial Workers

### Scheduler

- Source: None
- Github: https://github.com/Tracardi/com-tracardi
- Docker: tracardi/com-tracardi-scheduler-worker, tracardi/com-tracardi-scheduler
- Description: background processes for Pause and Result actions. This is basically as rq worker and rqscheduler from RQ
  library.

### Segmentation and Coping

- Source: com-tracardi/com_worker
- Github: https://github.com/Tracardi/com-tracardi
- Docker: tracardi/com-tracardi-segmentation-worker
- Redis Queue Worker that monitors the following queues:
    - segmentation:live,
    - event_to_profile_coping:worker,
    - event_props_to_event_traits:worker
- Description:
    - event_props_to_event_traits:worker is responsible for background coping of historical event properties to traits.
    - event_to_profile_coping:worker is responsible for background event to profile coping
    - segmentation:live is responsible for warning live segmentations. It is triggered by segmentation job.

## Commercial bridges

- Source: com-bridge-queue
- Github: https://github.com/Tracardi/com-bridge-queue
- Description: Queue bridges.

## Open-source Tracardi API

- Source:tracardi
- Github: https://github.com/Tracardi/tracardi-api
- Description: This is open-source Tracardi API responsible for collecting and processing events.

## Open-source Workers

- Source:tracardi/worker
- Github: https://github.com/Tracardi/tracardi-api
- Description: This is open-source Tracardi worker responsible for imports and system migration. 