# Tracardi plugin: String Validator

The purpose of this plugin is to validate data with custom regex.

# Configuration

This node require configuration.

* validation_regex - paste here your regex.
* data - here is data what we want to validate

# Examples

```json
{
  "validation_regex": "^h",
  "data": "hello!"
}
```

It will return TRUE

```json
{
  "validation_regex": "^a",
  "data": "hello!"
}
```

It will return FALSE

# Input payload

This node does not process input payload.

# Output

This is two output TRUE and FALSE.
