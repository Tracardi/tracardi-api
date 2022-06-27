# Start plugin

This plugin starts every workflow.

## Configuration

### Production run configuration

- Collect debugging information - Set if you want to collect debugging information. Debugging collects a lot of data if
  you no longer need to test your workflow disable it to save data and compute power.
- Trigger start on these event types - Workflow does not execute if incoming event type is not mentioned in this field.
  However, if left empty, workflow will be triggered regardless event type.

### Debug run configuration

- Profile-less event - enable this option if you want to test your workflow without profile data.
- Session-less event - enable this option if you want to test your workflow without session data attached.
- Event properties - You can manually specify event properties for debug purpose. However, this option does not apply if
  one of fields below are filled.
- Event ID - use this option if you want to test your workflow with one, particular event.
- Event type - use this option if you want to test your data with real event of selected type, instead of auto-generated
  one. Does not apply if Event ID field is filled.

```json
{
  "debug": "<bool>",
  "event_types": [
    {
      "id": "<event-type-1>",
      "name": "<event-type-1>"
    },
    {
      "id": "<event-type-2>",
      "name": "<event-type-2>"
    }
  ],
  "profile_less": "<bool>",
  "session_less": "<bool>",
  "properties": "<serialized-json>",
  "event_id": "<some-uuid>",
  "event_type": {
    "name": "<event-type-1>",
    "id": "<event-type-1"
  }
}
```