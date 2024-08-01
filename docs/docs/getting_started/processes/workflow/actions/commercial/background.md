# Run In Background

The Run In Background plugin allows you to run a whole workflow branch as a background task. It is designed to be used
as a starting node in the workflow.

## Description

The Run In Background plugin causes the entire workflow branch to be executed as a background task. It schedules the
task to run in the background and continues the workflow execution without waiting for the task to complete. This plugin
is part of the Tracardi Pro License.

# Inputs and Outputs

This plugin has one input:

- **payload** (dict): This port accepts a payload object.

This plugin has two outputs:

- **output**: This port is triggered when the background task is scheduled successfully. It returns an empty value.
- **error**: This port is triggered when an error occurs during the scheduling of the background task. It returns an
  error message along with the payload.

# Configuration

The configuration of the Run In Background plugin includes the following parameters:

- **Event type**: If you want the background task to be registered as a separate event type, you can specify the event
  type in this field. Leave it empty if you don't want to generate a separate event.
- **Event properties**: If you want the resumed workflow to receive different properties than the original event
  properties, you can specify them in this field. Leave it empty to resume the workflow with the original event
  properties.
- **Collect debugging information**: Enable this option if you want to collect debugging information during the
  background task execution. This option collects additional data for debugging purposes. Disable it if you no longer
  need to test your workflow to save data and compute power.

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Run In Background plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the scheduling of the background task. The error
  message provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port along with the payload.