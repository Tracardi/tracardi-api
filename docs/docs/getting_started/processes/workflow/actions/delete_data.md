# Delete data

This plugin is designed to remove specified data from the internal state of a workflow.

# Version

0.1

## Description

The Delete data plugin sequentially examines the list of fields provided by the user. If the field starts with "event@", the plugin issues a warning because event properties cannot be changed in the workflow and skips this value. For other provided values, the plugin attempts to delete this field from the internal state of the workflow. If the field is missing, a warning is issued. 

If the event is not a profile-less event, the profile is updated with any changes. If a session ID exists, the session is updated as well and the profile is saved in the profile cache. Finally, the payload, updated with the specified fields removed, is returned.

# Inputs and Outputs

The plugin accepts any JSON-like object as input through the "payload" port. After processing the payload and removing the chosen fields, the modified payload is then returned through the "payload" output port. The Delete data plugin can not initiate the workflow.

# Configuration

The configuration for the Delete data plugin consists of:
- __delete__ - A list of fields to be removed from the payload. These fields should be provided as dot notation referencing the internal state of the workflow.

# JSON Configuration

Here is a JSON example of the plugin configuration:
```json
{
  "delete": ["session@id", "profile@traits.private.email"]
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- "List to delete must not be empty." - This error is returned when the delete list, as provided in the configuration, is empty.
- "Could not delete value {value}, it is an event property and events can not be changed in workflow." - If a value that starts with "event@" is provided in the delete list, this warning is issued, as event properties cannot be deleted or changed during the workflow.
- "Could not delete value {value}, it is missing, details: {KeyError details}" - This is a warning message that is returned when a value in the delete list does not exist in the payload. The details of the KeyError exception are also reported in this warning.
   

It is important to note that even if warning messages are reported, the plugin execution will continue, and the remaining elements of the delete list will be processed. However, providing an empty delete list will result in a ValueError and halt the execution of the plugin.