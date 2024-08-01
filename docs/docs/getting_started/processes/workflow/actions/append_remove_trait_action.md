# Append/Remove data plugin

This plugin adds or removes values in arrays.

## Configuration

The following config:

```json
{
  "append": {
    "profile@traits.orders": "event@properties.order",
    "session@properties.list": "event@properties.property_list"
  },
  "remove": {
    "profile@traits.emails": "session@properties.email"
  }
}
```

Will:

- Append value from __event@properties.order__ to __profile@traits.private.orders__ list. If __profile@traits.private.orders__
  is not an array, then new array will be created, with current value as the only element.
- Append all values from __event@properties.property_list__ to __session@properties.list__.
- Remove value of __session@properties.email__ from __profile@traits.public.emails__ list. If __session@properties.email__ was
  also an array, then all elements from __session@properties.email__ would be removed from __profile@traits.public.emails__.