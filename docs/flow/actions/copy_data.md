# Copy data

This plugin copies event properties to a specified destination. It is a module that allows users to define a copying or
setting action to perform on data from an event to a profile. It is suitable for use in the data processing, collection,
and segmentation stages of workflows.

# Version

0.8.2

## Description

The Copy data plugin is a Tracardi plugin designed to copy data from event properties to a defined destination. When the
plugin is initialised, it validates its configuration settings and sets up the copying action based on these settings.

When an event occurs, the Copy data plugin checks the mapping defined in the
configuration. It loops through each configured destination, checks the value, and assigns it to the specified
destination.

Notably, the plugin is not capable of copying data to an event directly, as events are immutable and cannot be modified.
When a destination is an event, the plugin will skip that property and proceed with the rest.

If the event metadata contains a profile (i.e., the event is not profile-less) the plugin then checks for the presence
of a "traits" field in the profile. If it is not present or the "traits" field is not a dictionary, an error is
returned.

The plugin continues by comparing the initial and final state of the profile's "traits" field to check if any fields
were removed during the operation, which indicates a potential misconfiguration. It raises an error if such
inconsistencies are found.

Lastly, the plugin will replace the current session with the new session details. In
the end, the modified payload is returned.

# Inputs and Outputs

The "Copy data" plugin has one input:

- __payload__. This port accepts any JSON-like object.

The plugin has two outputs:

- __payload__ - Returns the given payload modified according to configuration.
- __error__ - Returns an error message if the copying operation could not be carried out.

# Configuration

The Copy data plugin's configuration contains a single property:

- __traits.set__ - Represents a dictionary of source and target data parameters for the copying or setting actions the
  plugin will carry out.

# JSON Configuration

Below is an example of a configuration setup:

```json
{
  "traits": {
    "set": {
    }
  }
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The following errors could be returned by the plugin.

- "Missing traits in profile" - This error occurs when the "traits" field is absent in the profile of the event.
- "Some values were not added to profile. Profile schema seems not to have path: {}. This node is probably
  misconfigured" - This error is raised if there are inconsistencies between the initial and final state of the
  profile's "traits" field. This is an indicator of a possible misconfiguration.
- Error when setting profile@traits to value __{}__. Traits must have key:value pair. E.g. __name__: __{}__ - This error
  occurs when the "traits" field is not a dictionary in the event's profile.
- "Profile changes were discarded in node 'Copy data'. This event is profile-less so there is no profile" - This warning
  is returned when the event does not have a profile (is profile-less), thus it is not capable of having profile
  changes.