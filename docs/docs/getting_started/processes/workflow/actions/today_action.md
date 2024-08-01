# Today

The "Today" plugin provides detailed information about the current date and time, including day of the week, month,
year, and exact time. This plugin is particularly useful for tasks that require date and time-related data processing.

# Version

0.8.2

## Description

The Today plugin operates by determining the current date and time based on a specified timezone. It then outputs
detailed information including the UTC time, local time, server time, and timestamps. The plugin can handle different
time zones, allowing for flexibility in workflows that involve users or events across various geographic locations.

## Inputs and Outputs

Inputs:

- Payload: Accepts any JSON-like object. The plugin uses this input to extract the specified timezone.

Outputs:

- Payload: Outputs a JSON object containing detailed current date and time information.
- Error: In case of issues, such as an unavailable time zone, this output provides an error message.

## Configuration

- __Timezone__: Specify the path to the field containing the timezone information. This can be a direct timezone string
  or a path using dot notation, such as "session@context.time.tz".

## JSON Configuration

Example configuration:

```json
{
  "timezone": "session@context.time.tz"
}
```

## Required resources

This plugin does not require external resources to be configured.

## Event prerequisites

The Today plugin is compatible with all event types and does not require synchronous events to operate.

## Errors

- "Unavailable time zone in current session": This error occurs if the specified timezone is not found or is invalid in
  the current session. The workflow will proceed through the "error" output port in this case.