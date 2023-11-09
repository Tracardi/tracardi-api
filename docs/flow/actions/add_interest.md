# Add Interest

The Add Interest plugin is used for adding interests to a user profile during a workflow processing.

# Version

0.8.0

## Description

The Add Interest plugin works by taking any payload as input and adding specific interests to a user profile. It is primarily used for segmentation and collection purposes in a workflow. 

The plugin begins by validating if a legitimate profile exists for the event. If the event is "profile less" or has no profile linked to it, the plugin outputs an error message and ends the process. If the profile is found, the plugin checks if the specified interest (from the plugin configuration) is already present in the profile's interests. 

If the interest is not present, the plugin updates the profile with the new interest value. The value of the interest is determined by the plugin configuration. If the specified interest is a list, the plugin makes sure to reshape the interest information by traversing this list. 

At the end of the process, the modified payload is returned. If an error occurs at any step, an error message indicating the reason is produced.

# Inputs and Outputs

The plugin accepts a **payload** at its input. It outputs through two ports: **payload** and **error**. 

The payload port outputs the input payload, while the error port is used to output error messages when exceptions are encountered during the process.

This plugin cannot start the workflow by itself; it needs a payload input to start a process.

# Configuration

The Add Interest plugin can be configured with two parameters:

- **Interest name**: This indicates the name of the interest you want to add to the user profile.
- **Interest value**: This denotes how much value you attach to the specified interest.

You need to provide values for these two parameters to properly configure the plugin.

# JSON Configuration

```json
{
  "interest": "music",
  "value": "1.0"
}
```

In the above configuration example, an interest named **music** is being added to the profile with a value of **1.0**.

# Required resources

This plugin does not require external resources to be configured.

# Errors

- "Can not add interests profile when processing profile less events." - This error is thrown when the plugin is run on an event that does not have a profile linked to it.
- "Can not add interests to empty profile." - This error means that the plugin cannot add interests to a non-existent profile.
- "Not acceptable interest type. Allowed type: string or list of strings" - This error indicates that the specified interest value isn't either of the accepted types. It should be a string or list of strings.