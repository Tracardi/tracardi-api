# Check conditions plugin
This plugin return results for conditions check.

## Configuration
It takes key-value pairs where value is a condition and key can be a string.

*Example*
```json
{
 "conditions": {
    "marketing-consent": "profile@consents.marketing EXISTS",
    "is-it-raining": "lowercase(payload@weather.condition)"
    }
}
```
## Input
This plugin takes any type of payload as input.

## Output

Plugin outputs object with conditions evaluated to false or true. 

Example:
```json
{
    "marketing-consent": true,
    "is-it-raining": false
}
```