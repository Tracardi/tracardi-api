# Merge event properties 

Automatically merges all event properties to profile traits.

# Version

0.8.1

## Description

This plugin is designed to merge event properties with the available profile traits. It does not take any decisions, but instead systematically merges all properties with existing traits. It is important to note that if there are existing traits that are the same as the properties, these traits will be updated with the new properties' values. 

The plugin operates by determining first if there is a profile available. Then, it locates where the properties should be merged within the profile traits using the user-defined path. The merging process may occur at the root of your profile traits if no sub-path is provided. Otherwise, a new sub-path can be created or an existing one can be updated if one is entered by the user.

The outcome of this merging process is refleted in the updated profile traits. 

# Inputs and Outputs

- `Input`: This plugin inputs a payload object.
- `Outputs`: This plugin outputs merged traits if the operation is successful. If no profile is available, an error will be generated.

# Configuration

The configuration of this plugin is quite simple, you only have one configuration parameter:
- `Sub traits path` : If you want to merge data to the root of your profile traits, leave this field empty. But if you intend to create or merge a specific part of the profile traits, type the sub-path in here. This path will be appended to the main traits path, e.g: `profile@traits[sub.path]`. 

# JSON Configuration

Example:

```
{
  "sub_traits": "sub.path"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- `error` : This error occurs when there is no available profile.

## Note

The merging process may replace existing values with new ones from the properties that are being merged, especially if they have the same keys. This is important to bear in mind when deciding which event properties to merge with the profile traits.