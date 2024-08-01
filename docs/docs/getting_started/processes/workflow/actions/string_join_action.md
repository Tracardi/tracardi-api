# Join string list

This plugin joins each element in the list with a given delimiter.

# Configuration

Example:

```json
{
  "string": ['a','b','c'],
  "delimiter": ","
}
```

This configuration will join each element in the list ['a','b','c'] with a given delimiter ','.
It converts the list into a string 'a,b,c'.
String can be provided as a path to data in profile, event, session, etc. Example of such configuration.

```json
{
  "string": "event@properties.data",
  "delimiter": ","
}
```

# Input

This plugin does not process input.

# Output

Returns the string converted from a string list using a given delimiter.

Example:

```json
{
  "result": "a,b,c"
}
```

