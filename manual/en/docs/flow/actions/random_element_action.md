# Return random item plugin

## Input
This plugin takes any payload object as input.

## Output
This plugin outputs a random value from provided list, accessible by key **value**.

## Configuration

This plugin takes a list of paths to fields containing values. It will
choose a list item randomly and return it. You can provide constant values as well.


```json title="Example"
{
  "list_of_items": [
    "value-1",
    "payload@value",
    "profile@traits.public.value"
  ]
}
```