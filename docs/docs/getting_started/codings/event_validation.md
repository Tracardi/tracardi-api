# Event validation schema

To add new event validation schema that you will need to provide a Json Schema object that defines the model of event,
or event session or loaded profile.

Validator consist of 2 elements. Data to be validated - expressed in a [dotted notation](dot_notation.md), and a
json schema itself.

```json
{
  "event@properties": {
    ...json-schema
  },
  "profile@traits.my-data": {
    ...json-schema
  }
}
```

## Example


```json title="Real example - for event@properties"
{
  "validation": {
    "json_schema": {
      "event@properties": {
        "type": "object",
        "properties": {
          "price": {
            "type": "number"
          },
          "name": {
            "type": "string"
          }
        },
        "required": [
          "name"
        ]
      }
    }
  },
  "event_type": "test"
}
```