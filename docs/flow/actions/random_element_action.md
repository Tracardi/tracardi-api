# Return random item

This plugin takes a list of values or references to field values, e.g. **profile@traits.public.value**. It will
choose an item randomly from the list and return it. If the value is a path to field it will be evaluated and the 
referenced value will be returned.

## Input
This plugin takes any payload object as input.

## Output
This plugin outputs a random value from provided list.

## Configuration

```json title="Example"
{
  "list_of_items": [
    "value-1",
    "payload@value",
    "profile@traits.value"
  ]
}
```

Result example

```
"value-1"
```

