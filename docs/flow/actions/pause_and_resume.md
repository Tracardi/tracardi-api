# Pause and resume

The Pause and Resume functionality allows you to temporarily stop the execution of a workflow and then resume its
operation after a specified period of time. This feature is useful when you need to introduce a delay or schedule
actions to be performed at a later time. The workflow can be resumed with the original event properties or with modified
properties if desired.

## Pausing the Workflow

To initiate a pause in the workflow, you need to provide the appropriate configuration parameters. The following
parameters are available:

* wait: This parameter specifies the duration (in seconds) for which the workflow should be paused before resuming. The
  workflow execution halts for this duration.

* event_type: This parameter allows you to specify an optional event type that can be registered when the workflow
  resumes. If no event type is specified, no event will be registered upon resumption.

* properties: If you wish to provide modified properties to the resumed workflow, you can specify them using this
  parameter. The properties should be provided in JSON format within the curly braces {}. If you want the workflow to
  resume with the original event properties, leave this field empty.

## Resuming the Workflow

After the specified pause duration has elapsed, the workflow automatically resumes its operation. Depending on the
configuration parameters, the workflow can be resumed with either the original event properties or the modified
properties.

If an event type was specified, a corresponding event will be registered in the system. If no event type was provided,
the resumption occurs as an internal system event without a separate registration. Example of JSON configuration.

```json
{
  "wait": 60,
  "event_type": {
    "id": "workflow-resumed",
    "name": "Workflow Resumed"
  },
  "properties": "{\"status\": \"pending\", \"retry_count\": 2}"
}
```

In this example, the workflow is paused for 60 seconds. After the pause, the workflow automatically resumes. The event
type "workflow_resumed" with the ID "123456" is registered. Additionally, the workflow is resumed with modified
properties, setting the status as "pending" and the retry count as 2.

## Does the Pause Event Impact Performance When the Workflow Runs for Several Days?

The pause event does not directly impact the performance of the current event process. When you pause an event, it is
sent to a background scheduled task and placed in a queue for completion. This means that the current event process
continues without being affected by the pause.

Once the pause time is finished, the event either resumes as a separate event if it has been configured as such, or it
resumes as an internal system event that is not recorded but processed. In either case, the response to the current
event is returned immediately, allowing the process to continue uninterrupted.

Overall, the pause event has minimal impact on the performance of the current event process, as it is handled separately
in the background without interrupting the ongoing operations.