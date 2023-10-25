# Sleep

The Sleep plugin is a time-based action plugin within Tracardi's workflow system. It pauses the workflow operation for a
certain duration, defined by the user in the plugin's configuration. This delay allows the system to wait a specified
number of seconds before proceeding to the next plugins.

# Version

0.1.2

## Description

Upon calling the Sleep plugin's "run" method, the system will pause for a designated time, specified in the plugin's
configuration field, 'wait'. The time unit is in seconds, and fractions of seconds can also be used.

The paused workflow will not process any additional actions or plugins during this wait time. Once the wait time is
completed, the plugin returns the same payload that was received, enabling the workflow to continue processing.

# Inputs and Outputs

Regarding the Sleep plugin's inputs and outputs - the plugin only has one port each for input and output, named '
payload'. The input payload can be any JSON-like object and it's passed to this plugin via the workflow. After the
pause, this payload is outputted exactly as it was received.

The Sleep plugin cannot start the workflow.

# Configuration

The Sleep plugin has only one configuration parameter:

- __wait__: The duration (in seconds) for which the workflow will pause before continuing processing. This value must be
  greater than or equal to zero. Fractions of seconds can be put into this field.

# JSON Configuration

Below is an example JSON configuration for the Sleep plugin:

```json
{
  "wait": 1
}
```

In this example, the Sleep plugin will pause the workflow for one second before returning the payload and continuing the
workflow.

# Required resources

This plugin does not require external resources to be configured.

# Errors

- __"Wait value has to be greater than or equal to 0."__: This error occurs when the value entered for 'wait' in
  configuration is less than zero. Sufficient time in seconds is essential for the plugin to correctly pause the
  workflow.