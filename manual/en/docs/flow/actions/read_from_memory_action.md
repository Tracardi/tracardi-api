# Read from memory plugin

This plugin allows you to read from cross-instance Tracardi user memory, using
given key.

## Requirements
Redis database has to be installed and running in order for this plugin to work.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns value on port **success** if the value was successfully read
from memory, or error detail on port **error** if one occurred.

## Configuration
#### With form
- Key - that's a key defined in usage of Write to memory plugin. This key points to
  data written to memory by Write plugin.

#### Advanced configuration
```json
{
  "key": "<key-to-value-in-memory>"
}
```