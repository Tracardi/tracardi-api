# Get previous event plugin

This plugin injects into payload one of the previous events from the current profile, according to given offset and event
type.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns event data on port **found** if the event was found, or input payload on port **not_found** if the
event was not found.

## Configuration

* Event type - an event type to be loaded into payload.
* Offset - an offset from current event. 0 will return current event, -1 will return previous one, etc.

#### Advanced configuration

```json
{
  "event_type": "<type-of-event-to-be-loaded>",
  "offset": "<offset-from-current-event>"
}
```