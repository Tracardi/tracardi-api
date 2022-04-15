# Get previous session plugin

This plugin fetches n-th last session of current profile and loads it into payload,
where n is defined by the offset parameter.

## Input
This plugin takes any payload as input.

## Outputs
- found - this port returns the session if it was found
- not_found - this port returns given payload if the session is not found

## Configuration
#### With form
- Offset - here provide an integer between -10 and 0 inclusively, where 0 is 
  current session, -1 is last session, etc.

#### Advanced configuration
```json
{
  "offset": "<number-of-wanted-session-counting-from-current-one>"
}
```