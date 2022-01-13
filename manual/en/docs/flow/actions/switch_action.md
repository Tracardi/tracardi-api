# Switch plugin

This plugin acts like a switch. It returns value, according to the value
of given field.

## Input
This plugin takes any payload object as input.

## Output
This plugin outputs one of values defined in config if condition value is present
in configuration, else **null**. Returned value looks like:
```json
{
  "value": "<returned-value>"
}
```

## Configuration

#### With form
- Condition value - That's the path to the field containing value that defines 
  returned value.
- Switch - Here provide key-value pairs, where key is the content of the condition field,
  and value is the value that will be returned when condition field's content meets with the key.

#### Advanced configuration
```json
{
  "condition_value": "<path-to-field-containing-condition-value>",
  "switch": {
    "payload@xyz": "<value1>",
    "<key1>": "profile@abc",
    "<key2>": "<value2>"
  }
}
```
In this case, if field specified in **condition_value** has the same value as
**payload@xyz**, then **value1** will be returned. If **condition_value** is
the same as **key1**, then value from field **profile@abc** will be returned, etc.
