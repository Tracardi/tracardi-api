# Event scheduler

This action will schedule an event to be triggered after given time.

# Configuration

```json
{
  "event_type": "<event-type>",
  "properties": {},
  "postpone": "+1m"
}
```

* *event_type* - type name of event type. e.g. 'page-view', 'purchase-order'.
* *properties* - event properties. This is a regular object with key value pairs. 
* *postpone* - for how long would you like the event to be postponed. For exmaple 1m means trigger event one minute after the action was executed.

# Input

This node does not process input data

# Output

Postponed task details. It will include the event iself with , context,profile, etc.


