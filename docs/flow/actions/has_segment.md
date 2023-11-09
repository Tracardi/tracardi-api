# Has Segment

The 'Has Segment' plugin is used to check if a given profile is part of a defined segment.

# Version

The version of this plugin is 0.7.3.

## Description

The 'Has Segment' plugin operates by checking whether a given profile (from incoming user event data) is included in a
specific segment. A segment, in this context, is a subgroup of profiles defined by specific characteristics or behavior.

The operation of the plugin is configured using a specific segment name. During the plugin operation, it checks whether
the defined segment is listed under the 'segments' attribute of the provided profile.

If the profile is found under the specified segment, the plugin returns the payload to the 'True' output port.
Otherwise, if the profile is not under the defined segment, or there is no profile data (profile-less event), the
payload is returned through the 'False' output port.

The plugin also generates console warnings or errors if the event does not have an associated profile (as in a
profile-less event) or if the profile value is empty. In either case, the payload will be returned through the 'False'
output port.

# Inputs and Outputs

The plugin accepts a payload of any type through its only input port, named 'payload'. The returned result, which also
contains the input payload, is sent through either of two output ports: 'True' or 'False'.

## Inputs

- __payload__: This port takes any payload. It represents the input data that the plugin will process.

## Outputs

- __True__: This port returns the input payload if the provided profile is found in the defined segment.
- __False__: This port returns the input payload if the provided profile is not found in the defined segment, or there
  is no profile data available.

# Configuration

The plugin has the following configuration parameter:

- __Segment__: This parameter represents the name of the segment that the plugin will check the profile against. It
  should be provided as a string and cannot be empty.

# JSON Configuration

Here is an example configuration for the plugin:

```json
{
  "segment": "Example Segment"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The following are potential errors that can occur during the operation of the plugin:

- __Segment cannot be empty__: This error occurs when the 'Segment' configuration parameter is provided as an empty
  string. Ensure that a valid segment name is specified in the configuration.
- __Can not check segment of profile when there is no profile (profileless event)__: This warning occurs when the plugin
  is trying to process a profile-less event. In such a case, the plugin will return the payload on the 'False' port.
- __Can not check segment profile. Profile is empty__: This error occurs when the profile data provided to the plugin is
  empty. In such a case, the plugin will return the payload on the 'False' port.