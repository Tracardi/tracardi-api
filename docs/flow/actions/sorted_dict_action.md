# Sort dictionary

Sorts the referenced dictionary and returns it as a list of tuples of key and value.

# Configuration

Example:

```json
{
  "data": {"first": 1, "second": 2, "fifth": 5, "third": 3},
  "direction": "asc",
  "sort_by": "key"
}
```

This configuration will sort the dictionary

```json
{"first": 1, "second": 2, "fifth": 5, "third": 3}
```

with the order provided by direction (default: "asc")

The dictionary is provided as a path to data in event. Example of such configuration.

```json
{
  "data": "event@properties.data",
  "direction": "asc",
  "sort_by": "key"
}
```

# Input

This plugin does not process input.

# Output

Returns the ordered list of tuples with keys and values.

Example:

```json
{
  "result": [
    ["first", 1], 
    ["second", 2], 
    ["third", 3], 
    ["fifth", 5]
  ]
}
```
