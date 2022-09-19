# Contains Pattern Plugin

This plugin checks if data field contains chosen pattern.

## JSON Configuration

Example config:

```json
{
  "field": "payload@field",
  "pattern": "all"
}
```

### Available patterns
* *url* - checks if data field contains exactly url for e.g. https://www.google.com 
* *ip* - checks if data field contains exactly ip address
* *date* - checks if data field contains exactly date in dd-mm-yyyy format
* *email* - checks if data field contains exactly email address
* *all* - checks if data field contains all the patterns listed above

Output:

Plugin outputs the payload on ports TRUE if field contains prefix or FALSE if otherwise.