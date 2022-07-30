# Log message plugin

This plugin logs message to flow logs.

## Input
This plugin takes any payload as input.

## Output
This plugin returns given payload on port **payload** without any changes.

## Configuration
```json
{
  "type": "warning | info | error",
  "message": "<your-message>"
}
```