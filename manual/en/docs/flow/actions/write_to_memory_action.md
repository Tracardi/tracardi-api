# Write to memory plugin

This plugin allows you to write to cross-instance Tracardi user memory, using
given key and value path.

## Requirements
Redis database has to be installed and running in order for this plugin to work.

## Input
This plugin takes any payload as input.

## Outputs
This plugin return payload on port **success** if the value was successfully written
to memory, or error detail on port **error** if one occured.

## Configuration
#### With form
- Key - that's a key to your data. Later you will be able to access your data with 
  it.
- Value - that's path to the value that you want to associate with given key.
- Time to live - that's a number of seconds, after which the value will be deleted.

#### Advanced configuration
```json
{
  "key": "<key-to-value-in-memory>",
  "value": "<path-to-value>",
  "ttl" : "<time-to-live-of-the-value>"
}
```