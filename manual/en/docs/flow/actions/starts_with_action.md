# StartsWith plugin

This plugin checks if payload field contains defined prefix by user

# JSON Configuration

Example input:

```json
{
   "field": "payload@field",
    "prefix": "string"
}
```

Output:

Plugin outputs the payload on ports TRUE or FALSE depends on function result.