# Day, Night split action

The purpose of this plugin is to split the workflow depending on day or night of its execution.

It will check if the event happened at day or night. Then it will route the workflow to the appropriate output port.

This action minds the time zone of the event. Therefore, you must provide time zone in configuration. By default, time
zone is included in browser event context.

# Configuration

This node requires configuration. In order to read timezone you must define path to time zone data. Use dot notation to
do that.

*Example*

```json
{
  "timezone": "session@context.time.tz"
}
```

# Input payload

This node does not process input payload.

# Output

This node has two output nodes. One for DAY route and one for NIGHT node. The DAY one is active when event happened at
day. The NIGHT node is active when it is night. 

Active output ports will return input payload. 
 
