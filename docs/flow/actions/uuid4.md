# UUID4 

UUID4 is a Tracardi plugin that generates a random UUID.

# Version

The documentation was created for the 0.6.2 version of the plugin.

## Description

The GetUuid4Action plugin serves one primary purpose - it generates a random UUID that can be used by other modules or stored for later use. The generation of UUID is carried out within the 'run' method, which executes the primary operation of the plugin.

The output of this action is in the form of a UUID that is passed through the 'uuid4' port. As an example, the generated UUID might look something like this: '123e4567-e89b-12d3-a456-426655440000'.

# Inputs and Outputs

The plugin accepts a payload object in its input port. The output port named 'uuid4' returns the generated UUID4.

Example of an input payload:

```json
{
  "example_key": "example_value"
}
```

Example of the output format:

```json
{
  "uuid4": "generated-uuid-string"
}
```

# Configuration

The UUID4 plugin does not require any configuration. 

# JSON Configuration

As the plugin does not require any configurations, an empty JSON object is used as an example:

```json
{}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

Since the plugin's sole function is to generate a random UUID and it does not have any set configurations, it does not usually raise exceptions or errors. However, errors might occur due to external issues like system irregularities or memory shortages.