# Append/Remove data plugin

This plugin adds or removes values in arrays.

## Configuration

The following config:

```json
{
  "append": {
    "profile@traits.private.orders": "event@properties.order",
    "session@properties.list": "event@properties.property_list"
  },
  "remove": {
    "profile@traits.public.emails": "session@properties.email"
  }
}
```

Will:

- Append value from `event@properties.order` to `profile@traits.private.orders` list. If `profile@traits.private.orders`
  is not an array, then new array will be created, with current value as the only element.
- Append all values from `event@properties.property_list` to `session@properties.list`.
- Remove value of `session@properties.email` from `profile@traits.public.emails` list. If `session@properties.email` was
  also an array, then all elements from `session@properties.email` would be removed from `profile@traits.public.emails`.