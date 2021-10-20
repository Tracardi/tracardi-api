# String Validator

This plugin validates data with regex pattern.

# Configuration

This node requires configuration.

* validation_regex - this is regex pattern.
* data - data what we want to validate. this value can also be a path to date in profile, session, event.

# Examples

```json
{
  "validation_regex": "^H",
  "data": "payload@properties.hello"   // This will return e.g. Hello world
}
```

It will return `{"result":true}`

```json
{
  "validation_regex": "^a",
  "data": "hello!"  // Now we use plain string instead of path to data.
}
```

It will return `{"result":false}`


# Input

This node does not process input payload.

# Output

This is two outputs `{"result":true}` and `{"result":false}`.
