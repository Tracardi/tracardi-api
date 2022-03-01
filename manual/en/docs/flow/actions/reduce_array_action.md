# Reduce array plugin

This plugin reduces given array.

## Input
This plugin takes any payload as input.

## Output
This plugin returns reduced array on port **result**, or some error info on port
**error** if one occurs.

#### Example input:
```json
{
  "list": ["a", "a", "a", "b", "b", "c"]
}
```
#### Output for this input:
```json
{
  "counts": {"a": 3, "b": 2, "c": 1},
  "max": "a",
  "min": "c"
}
```


## Plugin configuration
#### With form
- Path to array - here provide a valid dot path to array that you want to reduce.

#### Advanced configuration
```json
{
  "array": "<path-to-array>"
}
```
