# ContainsString Plugin

This plugin checks if data field contains defined prefix.

# JSON Configuration

Example input:

```json
{
  "field": "payload@field",
  "prefix": "string"
}
```

Output:

Plugin outputs the payload on ports TRUE if field contains prefix or FALSE if otherwise.