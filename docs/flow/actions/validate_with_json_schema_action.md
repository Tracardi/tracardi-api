# Validate with JSON schema plugin

The Validate with JSON schema plugin is used to validate objects using a provided JSON schema.

## Version

This documentation is based on version 0.7.4 of the Validate with JSON schema plugin.

## Description

The Validate with JSON schema plugin allows you to validate objects using a JSON schema. It takes a payload as input and
applies the specified JSON schema for validation. If the payload passes the defined validation, it is returned on the "
true" output port. If the payload fails the validation, it is returned on the "false" output port. If there is an error
in the validation schema itself, the payload is returned on the "error" output port.

The plugin uses the `EventValidator` class from the Tracardi domain to perform the validation. The JSON schema is
provided in the plugin's configuration and can be any valid JSON object.

## Inputs and Outputs

**Input**: payload (dict)

- This port accepts a payload object.

**Output**: true (dict)

- If the payload passes the defined validation, it is returned on this port.

**Output**: false (dict)

- If the payload fails the defined validation, it is returned on this port.

**Output**: error (dict)

- If there is an error in the validation schema itself, the payload is returned on this port.

## Configuration

The Validate with JSON schema plugin has the following configuration parameter:

- **JSON validation schema**: Specify a JSON validation schema that you want to validate the data with. Provide a valid
  JSON object as the schema.

## JSON Configuration

Here is an example of the JSON configuration for the Validate with JSON schema plugin:

```json
{
  "validation_schema": {
    "payload@properties.sale": {
      "type": "object",
      "properties": {
        "price": {
          "type": "number"
        },
        "name": {
          "type": "string",
          "maxLength": 15
        }
      }
    },
    "profile@context.timestamp": {
      "type": "integer"
    }
  }
}
```

## Required resources

This plugin does not require external resources to be configured.

## Errors

The Validate with JSON schema plugin may raise the following exception:

- **EventValidationException**

  This exception occurs if the payload does not pass the defined validation or if there is an error in the validation
  schema itself.