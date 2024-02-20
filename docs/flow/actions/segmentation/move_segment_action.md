# Move segment

This plugin allows for the transition of a profile from one segment to another, effectively updating the profile's
segmentation in the process.

# Version

0.8.1

## Description

The Move Segment plugin is designed to facilitate the reclassification of profiles within different segments. This
operation involves removing the profile from an existing ("from") segment and adding it to another ("to") segment.
During this process, the plugin ensures that the profile's segment list is unique and up-to-date. If the profile is
already part of the "from" segment, it will be removed from that segment. Conversely, if the profile is not yet a part
of the "to" segment, it will be added. This resegmentation reflects immediately in the profile's metadata, marking the
time of segmentation to the current UTC time. The plugin ensures that profiles maintain relevant and accurate segment
associations by moving them between segments as needed.

# Inputs and Outputs

## Inputs:

- **payload**: The plugin accepts any form of payload, which is passed through unchanged.

## Outputs:

- **payload**: The original payload is returned, indicating that the data flow remains unaffected by the plugin's
  operations.

# Configuration

- **Move from segment**: The name of the segment from which the profile is to be moved. This field must be filled out to
  identify the source segment accurately.
- **Move to segment**: The name of the segment to which the profile is to be moved. This field must also be filled out
  to define the target segment for the reclassification.

# JSON Configuration

```json
{
  "from_segment": "current_segment_name",
  "to_segment": "target_segment_name"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The Move Segment plugin is compatible with all event types, facilitating its integration into various workflow scenarios
without the need for synchronous event processing.

# Errors

- **"Segment cannot be empty"**: This error occurs if either the "from_segment" or "to_segment" configuration fields are
  left empty. A valid segment name is required for both the source and target segments to ensure the plugin can execute
  its function correctly.

Through the application of the Move Segment plugin, users are empowered to dynamically manage and update profile
segmentations, ensuring that profiles are always associated with the most relevant segments according to their latest
interactions or behaviors.