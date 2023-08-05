# Event Counter

The Event Counter plugin reads how many events of a defined type were triggered within a specified time frame.

## Description

The Event Counter plugin is designed to count the number of events of a specific type that occurred within a defined
time span. This plugin can be useful for tracking and monitoring event activity and analyzing event patterns.

When the plugin is executed, it retrieves the specified event type and time span from the plugin's configuration. It
then queries the event database to count the number of events of the specified type that occurred within the specified
time span. The plugin returns the count of events as the output.

This documentation is for version 0.8.1 of the Event Counter plugin.

# Inputs and Outputs

The Event Counter plugin has one input:

- `payload` (object): This port accepts a payload object.

The Event Counter plugin has one output:

- `payload` (object): Returns the number of events of the specified type within the defined time span.

Example:

Input:

```json
{
  "payload": {}
}
```

Output:

```json
{
  "payload": {
    "events": 42
  }
}
```

# Configuration

The Event Counter plugin requires the following configuration:

- `Event type`: Select the event type you would like to count.
- `Time span`: Enter the time span in a format like "-15minutes" to define the period for counting the events.

# JSON Configuration

Here is an example of a JSON configuration for the Event Counter plugin:

```json
{
  "event_type": {
    "name": "example_event",
    "id": "example_event_id"
  },
  "time_span": "-15m"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Event Counter plugin may raise the following exceptions:

- `ValueError: profile event sequencing cannot be performed without a profile. Is this a profile-less event?`: This
  error occurs when the plugin attempts to perform profile event sequencing without a profile. Make sure the event
  contains a profile.
- `Some other exception`: This error occurs when some other exception is raised during the execution of the plugin.

Note: The specific conditions that may trigger these errors depend on the context and usage of the plugin within the
workflow.