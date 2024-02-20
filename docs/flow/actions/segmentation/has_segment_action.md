# Has segment

This plugin checks if a profile is part of a defined segment. If the profile is in the specified segment, the workflow
will continue along the "True" path; otherwise, it will proceed along the "False" path.

# Version

0.7.3

## Description

The Has Segment plugin serves a conditional role within a workflow, determining the path of execution based on the
profile's membership in a specified segment. Upon execution, the plugin examines the profile's segment list to check for
the presence of the configured segment. If the profile includes the specified segment, the plugin outputs the payload
through the "True" port, indicating that the condition has been met. If the segment is not found, the payload is
returned through the "False" port, suggesting the condition has not been fulfilled. This functionality is essential for
workflows that require conditional logic based on profile segmentation, allowing for more personalized and targeted
actions within the workflow.

# Inputs and Outputs

## Inputs:

- **payload**: Accepts any form of payload, which is passed through the plugin without modification.

## Outputs:

- **True**: The output port used if the profile is in the defined segment. It returns the input payload.
- **False**: The output port used if the profile is not in the defined segment. It also returns the input payload.

# Configuration

- **Profile segment to check**: The name of the segment you wish to check against the profile. This configuration must
  be specified to identify the target segment for the check.

# JSON Configuration

```json
{
  "segment": "specified_segment_name"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The plugin works with all types of events. It is designed to function within workflows regardless of the event's
synchronous or asynchronous nature, making it versatile for various use cases.

# Errors

- **"Segment cannot be empty"**: This error occurs if the segment configuration is left empty. A segment name is
  required for the plugin to perform its function effectively. This validation ensures that the plugin has a specific
  segment to check for within the profile.

By incorporating the Has Segment plugin into a workflow, users can implement conditional logic based on profile
segmentation, enabling more granular control over the workflow's execution path based on profile characteristics.