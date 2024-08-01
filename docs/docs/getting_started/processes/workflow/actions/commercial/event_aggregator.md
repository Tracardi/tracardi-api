# Event Aggregator

This plugin collects and tallies up the occurrences of a specific category of information during a certain period of
time for the current profile.

## Description

The Event Aggregator plugin counts how many times something happens for the current profile over a defined amount of
time. It aggregates events based on a specified field and returns the aggregation result.

This documentation is for version 0.8.1 of the plugin.

## Inputs and Outputs

### Inputs

- `payload`: This port accepts a payload object.

### Outputs

- `payload`: Returns the aggregation result.

## Configuration

The Event Aggregator plugin requires the following configuration:

- **Aggregate by field**: Select the field you would like to aggregate. This field determines the category of
  information for which the occurrences will be counted. The available options are retrieved from
  the `/storage/mapping/event/metadata` endpoint.

- **Time span**: Specify the time span over which the occurrences will be counted. Enter the time span in a format
  like `-15minutes`. This field determines the period of time during which the events will be aggregated.

## JSON Configuration

Here is an example JSON configuration for the Event Aggregator plugin:

```json
{
  "field": {
    "name": "example_field",
    "id": "example_field_id"
  },
  "time_span": "-15m"
}
```

## Required Resources

This plugin does not require external resources to be configured.

## Errors

- **Profile ID not found**: The profile ID is not found or is not correctly configured. This error may occur if the
  profile ID is set to `@debug-profile-id`. Make sure to load the correct profile to ensure that the plugin can find the
  necessary data.

- **Event field not specified**: The aggregate by field is not specified in the configuration. This error may occur if
  the "Aggregate by field" configuration field is left empty. Please select a field to aggregate.

- **Invalid time span format**: The specified time span format is invalid. This error may occur if the "Time span"
  configuration field is not formatted correctly. Make sure to enter the time span in a valid format, such
  as `-15minutes`.