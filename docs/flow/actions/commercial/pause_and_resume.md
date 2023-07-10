# Pause and Resume

The "Pause and Resume" plugin in Tracardi allows you to pause the workflow for a specified duration and then resume it at the same node. This plugin is useful for introducing delays or scheduling events within a workflow.

## Description

The "Pause and Resume" plugin is a time-based plugin that waits for a specified number of seconds and then resumes the workflow. During the pause, no actions or transitions occur in the workflow. Once the pause is complete, the workflow continues from the same node where it was paused.

## Inputs and Outputs

- **Input**: This plugin accepts any payload as input.

- **Output Ports**:
  - **output**: This port is triggered when the pause is complete, indicating that the workflow can resume.
  - **error**: This port is triggered if an error occurs during the execution of the plugin.

## Configuration

The "Pause and Resume" plugin has the following configuration options:

- **Wait in seconds**: This parameter specifies the duration of the pause in seconds. The plugin will wait for the specified number of seconds before resuming the workflow.

- **Event type**: If you want the resumed workflow to be registered as a separate event type, you can specify the event type in this field. Otherwise, leave it empty, and no event will be generated when the workflow resumes.

- **Event properties**: If you want the resumed workflow to have different properties than the original event, you can specify them here. Otherwise, leave it empty, and the workflow will resume with the original event properties.

- **Collect debugging information**: Enable this option if you want to collect debugging information during the execution of the workflow. Debugging information includes additional data for testing and troubleshooting purposes.

## Example Usage

Here's an example of how the "Pause and Resume" plugin can be used:

```yaml
- pause_and_resume:
    wait: 60
    event_type:
        id: "custom-event"
        name: "Custom Event Type"
    properties: '{"custom_property": "value"}'
    debug: true
```

In this example, the plugin is configured to pause the workflow for 60 seconds. After the pause, the workflow will resume from the same node. The resumed workflow will generate a custom event of type "Custom Event Type" with the specified custom properties. Debugging information will also be collected during the execution of the workflow.

