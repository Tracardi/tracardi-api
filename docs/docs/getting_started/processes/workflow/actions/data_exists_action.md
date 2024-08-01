# Data check action

This plugin check if data exists and is not null or empty.

Type the path to property to be checked.

Example:
```
{
  "property": "event@context.page.url"
}
```

This will check if `context.page.url` exists in event.


# Input payload

This node does not input payload.

# Output

* __True__ - This port is triggered if the data exists.
* __False__ - This port is triggered if the data does not exist.