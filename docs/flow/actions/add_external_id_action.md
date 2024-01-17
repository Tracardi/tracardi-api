# Add Integration Id

This plugin is designed to create a link between Tracardi profiles and their corresponding identities in external
systems. It's useful for keeping a reference to the profile in an external system for easy lookup.

# Version

0.8.2

## Description

The Add Integration Id plugin allows you to associate an external system's ID with a Tracardi profile. It works by
taking an ID and optional additional data from the payload or event and adds this information to the profile's metadata
under a specified external system name. This is particularly useful when you have profiles that exist in Tracardi and
another external system, and you want to maintain a reference between the two. The plugin also updates the profile to
reflect these changes.

## Inputs and Outputs

- __Inputs:__
    - __payload:__ This input accepts a payload object which should contain the necessary data for the plugin to
      process.

- __Outputs:__
    - __payload:__ If the operation is successful, it returns the original payload object.
    - __error:__ In case of any failure, an error message is returned.

The plugin does not initiate a workflow; it acts on the data passed to it.

## Configuration

- __External ID:__ A reference to the external ID that you want to link with the Tracardi profile.
- __External System Name:__ The name of the external system where the referenced ID originates.
- __Additional Data:__ Optional data related to the external system. This can be any data from the event or payload that
  you want to associate with the external ID.

# JSON Configuration

```json
{
  "id": "event@properties",
  "name": "External System",
  "data": "{\"key\": \"value\"}"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The Add Integration Id plugin works with all types of events and does not specifically require synchronous events.

# Errors

- __"Id can not be empty."__: Occurs when the External ID is not provided in the configuration.
- __"Name can not be empty."__: Happens if the External System Name is left blank in the configuration.
- __Errors during JSON processing or reshaping__: These errors will occur if there is an issue with the additional data
  JSON format or during the reshaping process. They will be returned as a general exception message.

This plugin enhances the capability of Tracardi to integrate and associate profiles with external systems, thereby
extending its utility in complex system environments.
