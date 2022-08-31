# ContainsString Plugin

This plugin checks if data field contains defined substring.

## JSON Configuration

Example config:

```json
{
  "field": "payload@field",
  "substring": "string"
}
```

Output:

Plugin outputs the payload on ports TRUE if field contains prefix or FALSE if otherwise.