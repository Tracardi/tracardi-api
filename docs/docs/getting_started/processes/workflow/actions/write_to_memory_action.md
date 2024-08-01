# Write to memory plugin

This plugin allows you to write to cross-instance Tracardi user memory, using
given key and value path.

## Requirements
Redis database has to be installed and running in order for this plugin to work.

## Input
This plugin takes any payload as input.

## Outputs
This plugin return payload on port **success** if the value was successfully written
to memory, or error detail on port **error** if one occurred.

## Configuration

- Key - A name of the variable that will hold saved data.
- Value - Any string or reference to data inside workflow. This can be an object, or any value. 
- Time to live - The number of seconds, after which the value will be deleted.

#### Advanced configuration
```json
{
  "key": "<key-to-value-in-memory>",
  "value": "<path-to-value>",
  "ttl" : "<time-to-live-of-the-value>"
}
```