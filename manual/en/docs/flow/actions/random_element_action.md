# Return random item plugin

## Input
This plugin takes any payload object as input.

## Output
This plugin outputs a random value from provided list, accessible by key **value**.

## Configuration

#### With form
- List of items - here provide a list of paths to fields containing values, that plugin will
  choose randomly from. You can provide constant (not-path) values as well.

#### Advanced configuration
```json
{
  "list_of_items": [
    "<example-path-1>",
    "<example-path-2>",
    "<constant-value-1>",
    "<constant-value-2>"
  ]
}
```