# Local time span action

The purpose of this plugin is to check if the local time is within 
defined time span.

This action minds the time zone of the event. Therefore, you must provide 
time zone. By default, time zone is included in browser event context. 


# Configuration

This node requires configuration. In order to read timezone 
you must define path to it. Use dot notation to do that.

Moreover, you need to set start and end of the time span. The time slots 
have no default values. 

Example of the configuration:

```json
{
  "timezone": "session@context.time.tz",
  "start": "12:00:00",
  "end": "14:00:00"
}
```

# Input

This node does not process input payload.

# Output

Return input payload on IN port or OUT port. Returns data on IN port if local time is in defined time span.