# Time Delay

This plugin calculates a date based on a specified date and a time delay. It can either add or subtract the delay, which
is defined in seconds.

# Version

0.8.2

## Description

The Time Delay plugin is designed to calculate a new date by adding or subtracting a specified delay from a reference
date. This plugin takes a date, which can be either a specific datetime object or a string, and applies a time delay to
it. The delay can be added or subtracted based on the user's choice.

The process starts by receiving a payload. The plugin then extracts the reference date from the payload using dot
notation, a method that retrieves data from the workflow's internal state. This reference date is either a specific
datetime object or a string like 'now', which represents the current date and time.

Next, the plugin calculates the new date by adding or subtracting the specified delay, in seconds, from the reference
date. This calculation depends on the chosen operation (addition or subtraction). The result is a new date, which is
then returned as the output of the plugin.

# Inputs and Outputs

Inputs:

- __payload__: This is the input payload object from which the reference date is extracted.

Outputs:

- __date__: This output port returns the calculated date after applying the time delay.
- __error__: In case of any errors during the process, this output port returns an error message.

# Configuration

- __Reference Date__: Path to the date in the payload, specified in dot notation.
- __Operation__: Choice of operation, either to add or subtract the delay.
- __Delay__: The time delay in seconds to be added or subtracted from the reference date.

# JSON Configuration

```json
{
  "reference_date": "profile@metadata.time.insert",
  "sign": "+",
  "delay": "60"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

This plugin works for all types of events and does not require the event to be synchronous.

# Errors

- "Could not parse data __{date}__": This error occurs if the plugin is unable to parse the provided date.
- "Date can be either string or datetime object": This error is raised if the provided date is neither a string nor a
  datetime object.
- Any other exceptions will return a general error message containing the exception's text. This typically occurs if
  there are issues with the payload or the configuration parameters.

This documentation provides a comprehensive overview of the Time Delay plugin, detailing its functionality,
configuration, and potential errors. It's designed to be understandable even for individuals without technical
background in coding or software development.