# Mask data

This plugin masks the contents of specified profile traits, replacing them with a "###" character sequence. This allows for data obfuscation or masking whenever necessary.

# Version

The version of this plugin is 0.7.0.

## Description

The Mask data plugin takes a payload and masks the contents of traits specified in the configuration. Instead of their original content, these traits have their values replaced with a "###" character sequence.

When running, the plugin first accesses the payload's dot notation through the `_get_dot_accessor` method. Then for each trait specified in the configuration, it checks the data source. If the data source is either 'flow' or 'event', the trait data cannot be modified and a warning message is logged to the console. Another warning is logged if a specified trait is either invalid or doesn't exist.

If none of the above issues occur, the trait's value is replaced with "###". If there is profile or session data in the payload, the original profile or session is replaced with an updated version that includes the masked traits.

The plugin then returns the payload with the masked trait data back into the workflow.

# Inputs and Outputs

The Mask data plugin has only one input and one output port:

Inputs:
- **payload**: This port accepts a payload object. Depending on the payload content and the plugin configuration, some traits of the payload might get masked.
   
Outputs:
- **payload**: This port returns the same payload object that was passed as input, but with some traits masked, depending on the configuration.

Note: This plugin cannot be used as a starting node in a workflow.

# Configuration

- **traits**: A list of strings representing the traits to be masked. These traits should be specified in a dot notation format and will be replaced with "###".

# JSON Configuration

Here is an example of JSON configuration for the Mask data plugin:
```json
{
    "traits": ["profile@trait1", "session@trait2"]
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- If the source of a trait to be masked is either 'event' or 'flow', the trait values cannot be modified in the workflow. In such a case, a warning "Event/Flow values cannot be hashed." will be logged.
  
- If a specified trait is either invalid or does not exist, a warning "Given trait {trait} is invalid or does not exist." will be logged. Note that the "{trait}" placeholder will be replaced with the actual trait in the log.

Remember to validate your configuration before running a workflow with this plugin. Inaccurately defined traits will lead to warnings and may cause the plugin to not properly mask the desired data.