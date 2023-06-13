# Can you describe Tracardi components?

## Commercial Tracardi API

- Source: com-tracardi/com_tracardi, tracardi/tracardi
- Docker: tracardi/com-tracardi-api
- Description: This is commercial Tracardi API responsible for collecting and processing events

## Commercial Jobs

### Heartbeats

- Source: com-tracardi/com_job/heartbeat
- Docker: tracardi/com-heartbeat-job
- Description: This job is responsible for running some defined event on all profiles. It has defined strategies such
  as:
    - inactive-profile: Gets profiles if no event happened in `wait_period` time and there was no event
      type `event_type` E.g. This allows to raise for example an event `inactive` if no activity on profile in 2 days
      and no `inactive` event available in all profile events.
    - inactive-session:  Gets session if no event happened in `wait_period` time and there was no event
      type `event_type`. E.g. This allows to raise for example an event `inactive` if no activity in 15 min and
      no `inactive` event available within the session
    - session-not-closed: Gets all profiles if there is no event for a defined period (15 min) and raise session 
      closed event.

### Live Segmentation

- Source: com-tracardi/com_job/segmentation
- Docker: tracardi/com-tracardi-segmentation-job
- Description: Iterate over live segmentation flows. 


Commercial Workers

- Source: com-tracardi/com_worker
- Docker: tracardi/com-tracardi-segmentation-worker
- Redis Queue Worker that monitors the following queues:
    - segmentation:live,
    - event_to_profile_coping:worker,
    - event_props_to_event_traits:worker
- Description:
    - event_props_to_event_traits:worker is responsible for background coping of historical event properties to traits.
    - event_to_profile_coping:worker is responsible for background event to profile coping
    - segmentation:live is responsible for warning live segmentations. It is triggered by segmentation job.