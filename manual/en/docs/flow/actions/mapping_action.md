# Switch plugin

This plugin maps value to one of the item from a set of values. It returns value, according to the value
of given field.

## Input
This plugin takes any payload object as input.

## Output
This plugin outputs one of values defined in config if it matches its key
in the provided set of key-value pairs, else **null**. Returned value looks like:
```json
{
  "value": "<returned-value>"
}
```
Configuration takes a __value__ and a set of data defined in __switch__ property. 


```json title="Example"
{
  "value": "<path-to-field-containing-condition-value>",
  "switch": {
    "payload@xyz": "value1",
    "key1": "profile@abc",
    "key2": "value2"
  }
}
```
In this case, where the field specified in **value** has the same value as
**payload@xyz**, then **value1** will be returned. If **value** is
the same as **key1**, then value from field **profile@abc** will be returned, etc.
