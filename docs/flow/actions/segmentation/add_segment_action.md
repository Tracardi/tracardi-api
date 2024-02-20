# Add segment

This plugin enables adding a specific segment to a profile. When activated, it appends the designated segment or
segments to the profile, helping categorize or tag profiles based on specific criteria or behaviors.

# Version

0.8.1

## Description

The Add Segment plugin is designed to enhance profile segmentation by adding predefined segments to a profile. This
process involves checking the profile's current segments and adding new ones if they are not already present. The plugin
operates by examining the incoming payload and the specified segment configuration. If the targeted segment(s) are not
part of the profile's existing segments, they are added, and the profile's segmentation timestamp is updated to the
current UTC time. The plugin supports both single segments (as a string) and multiple segments (as a list of strings).
It employs a dynamic approach to handle the addition of segments, ensuring that the operation can adapt based on the
provided segment configuration. The output of the plugin is the original payload, indicating that the primary purpose of
the plugin is to update the profile's segmentation without altering the workflow's data flow.

# Inputs and Outputs

The plugin accepts any payload through its input port and returns the input payload unchanged through its output port,
labeled "payload". This design signifies that the plugin's primary function is to update the profile's segmentation
based on the specified configuration without modifying the incoming data.

## Inputs:

- **payload**: Accepts any payload object, serving as a pass-through for the workflow data.

## Outputs:

- **payload**: Returns the input payload, indicating the plugin's operation does not alter the data flow.
- **error**: Outputs error information if issues occur during the segment addition process.

# Configuration

- **Segment name**: The name of the segment to be added to the profile. This can be a single segment name (string) or a
  list of segment names (list of strings). The plugin validates that this configuration is not empty to ensure a segment
  is specified for addition.

# JSON Configuration

```json
{
  "segment": "example_segment_name"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The plugin works with all types of events. It does not have a specific requirement for the event to be synchronous or
asynchronous, making it versatile for various workflow scenarios.

# Errors

- **"Segment cannot be empty"**: This error occurs if the segment configuration is left empty. The plugin requires at
  least one segment name to function correctly.
- **"Not acceptable segmentation type. Allowed type: string or list of strings"**: This error is triggered if the
  provided segment configuration is neither a string nor a list of strings. The plugin is designed to handle these two
  types for segment addition.
- **KeyError**: This exception might happen if there's an issue accessing the segment data within the provided payload
  or configuration. It indicates a mismatch or absence of expected data paths.