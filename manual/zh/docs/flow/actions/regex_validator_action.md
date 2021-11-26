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

It will return `payload` on `valid` output port. `invalid` port will stay inactive. 

```json
{
  "validation_regex": "^a",
  "data": "hello!"  // Now we use plain string instead of path to data.
}
```

It will return `payload` on `invalid` output port. `valid` port will stay inactive. 


# Input

This node does not process input payload.

# Output

This plugin has to port valid and invalid. Depending on validation result the appropriate ports will be launched with payload copied as data.
