# Delete segment

This plugin facilitates the removal of a specified segment from a profile. When activated, it identifies and deletes the
designated segment from the profile's segment list, if present.

# Version

0.8.1

## Description

The Delete Segment plugin is designed to streamline the process of managing profile segmentation by allowing for the
removal of specific segments from a profile. Upon execution, the plugin checks if the specified segment exists within
the profile's current segment list. If found, the segment is removed, and the profile's segmentation timestamp is
updated to reflect the change at the current UTC time. This operation is essential for maintaining accurate and
up-to-date segmentation information within profiles, ensuring that profiles are only associated with relevant segments.
The plugin operates seamlessly, requiring only the name of the segment to be removed as input and returning the original
payload, thereby indicating that the main function of the plugin has been executed without altering the workflow's data
flow.

# Inputs and Outputs

## Inputs:

- **payload**: Accepts any payload object, serving as a conduit for data flow within the workflow.

## Outputs:

- **payload**: Outputs the original payload, signifying that the primary function of the plugin is the modification of
  the profile's segments rather than the data itself.

# Configuration

- **Segment name**: The name of the segment you wish to remove from the profile. This field must be filled in to
  identify the specific segment targeted for deletion. The plugin ensures that this configuration is not left empty to
  prevent operational errors.

# JSON Configuration

```json
{
  "segment": "specified_segment_name"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The Delete Segment plugin can be utilized with all types of events, without any specific requirement for the event to be
synchronous. It is suitable for integration into various workflow scenarios, providing flexibility in its application.

# Errors

- **"Segment cannot be empty"**: This error occurs if the segment name is not provided in the configuration. A segment
  name is required for the plugin to perform its function correctly. This validation ensures that the plugin has a
  specific target for segment deletion.

