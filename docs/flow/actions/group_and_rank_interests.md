# Group and Rank Interests

This plugin gets profile interests and computes new segments based on the defined schema. 

# Version

This documentation is for version 0.9.0 of the plugin.

## Description

The Group and Rank Interests plugin works by taking a profile's interests, mapping them into segments, and then applying
the most relevant segments to the profile. Here's how it does this step by step:

1. The plugin first loads the profile's interests and the segment mapping. Segment mapping defines how different
   interests are grouped into segments.
2. It calculates the total count of interests for each segment. For example, if a profile has interests in "iphone", "
   ipad", and "imac", and these are grouped into an "apple-fan-boy" segment, it sums up the counts of these interests.
3. The plugin then ranks these segments based on their total interest counts.
4. Depending on the configured threshold (segments to apply), it selects the top-ranked segments and applies them to the
   profile.

For instance, if a profile has interests in various gadgets, and the threshold is set to 3, only the top 3 segments with
the highest interest counts will be applied to the profile.

# Inputs and Outputs

- **Inputs:** This plugin takes a payload object as its input.
- **Outputs:** It has two outputs:
    - **Result:** Outputs the segments applied to the profile.
    - **Error:** Outputs an error message if the plugin encounters any issues during execution.

This plugin does not start the workflow.

# Configuration

- **Interests:** Location within the profile where interests are stored, usually referenced as __profile@interests__.
- **Segment Mapping:** Defines how segments are constructed based on profile interests. It maps each segment name to a
  list of interests that contribute to that segment.
- **Segments To Apply:** This setting decides how many of the top-ranked segments, based on their total interest counts,
  should be applied to the profile. For example, if set to 5, only segments whose total interest count is among the top
  5 will be applied.

# JSON Configuration

```json
{
  "interests": "profile@interests",
  "segment_mapping": "{\"segment_name\": [\"interest1\", \"interest2\"]}",
  "segments_to_apply": "5"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

This plugin works for all types of events and does not require the event to be synchronous.

# Errors

- **Interests must not be empty:** This error occurs if the interests field is left empty or only contains whitespace.
- **Segment Mapping must not be empty:** This error is raised if the segment mapping is not provided.
- **Segments to Apply must not be empty and must be a number:** Occurs if the segments to apply field is either empty,
  contains only whitespace, or is not a valid number.
- **Segments To Apply must be a number:** This message is returned if the segments to apply configuration is not a valid
  number, indicating a configuration error.