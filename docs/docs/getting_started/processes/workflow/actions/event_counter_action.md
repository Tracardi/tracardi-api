# Event counter

This plugin reads how many events of a defined type were triggered within a defined time.

## Description

The Event counter plugin is designed to count the number of events of a specific type that occurred within a specified
time frame. It retrieves the event count based on the provided configuration and returns the result.

This documentation is based on version 0.8.1 of the Event counter plugin.

# Inputs and Outputs

## Inputs

The Event counter plugin accepts the following input:

- **payload**: This port accepts a payload object.

## Outputs

The Event counter plugin provides the following outputs:

- **payload**: Returns the number of events of the defined type.

Example output:

```json
{
  "events": 39
}
```

# Configuration

The Event counter plugin supports the following configuration parameters:

- **Event type**: Select the event type you would like to count.
- **Time span**: Specify the time span to search for events. Use the format "-15minutes" to indicate a time span of 15
  minutes in the past.

# JSON Configuration

Here is an example JSON configuration for the Event counter plugin:

```json
{
  "event_type": "page-view",
  "time_span": "-15m"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Event counter plugin may encounter the following errors:

- **ValueError: Invalid time span**: This error occurs when the specified time span is invalid or cannot be parsed.
  Ensure that the time span is formatted correctly, such as "-15m".
- **Event type not specified**: This error occurs when the event type is not provided in the configuration. Make sure to
  select an event type from the available options.

