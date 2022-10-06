# String splitter

This plugin splits any string with a given delimiter.

# Configuration

Example:

```json
{
  "string": "a.b.c",
  "delimiter": "."
}
```

This configuration will split `a.b.c` string into ["a", "b", "c"], using '.' as delimiter.
String can be provided as a path to data in profile, event, session, etc. Example of such configuration.

```json
{
  "string": "event@properties.data",
  "delimiter": "."
}
```


# Input

This plugin does not process input.

# Output

Returns array with separated values.

Example:

```json
{
  "result": [
    "a",
    "b",
    "c"
  ]
}
```

