# JSON to data

The JSON to data plugin is designed to convert a JSON string to data objects. It serves as a converter, simplifying the
process of dealing with JSON strings in your workflow.

# Version

The documentation was created for version 0.6.2 of the plugin.

## Description

The JSON to data plugin works by accepting a JSON string, specified by a reference path, and converting it into data
objects. This process is executed within the "run" method of the plugin. The reference path to the JSON string is
extracted from the plugin's configuration. Once the JSON string is obtained, it attempts to convert it into a data
object.

If the JSON string is valid and was correctly converted into a data object, the plugin returns this data on the "
payload" output port. If the conversion fails, likely due to an issue with the JSON string (é.g., malformed syntax),
then an error message is returned on the "error" output port.

# Inputs and Outputs

This plugin processes and accepts inputs on the "payload" input port which receives the workflow payload.

It has two output ports, 'payload', and 'error'. If the JSON string was correctly converted into data objects, the new
data is returned on the "payload" port. This output consists of a dictionary, with the key "value" and the value being
the converted data object. Example of successful operation:

```json
{
  "value": {
    "converted": "data objects here..."
  }
}
```

If the conversion fails, an error message is returned on the "error" output port. This returned error contains the
original payload. Example:

```json
{
  "value": {
    "original": "payload here..."
  }
}
```

The plugin cannot initiate the workflow.

# Configuration

The configuration for this plugin is straightforward. It consists of one parameter:

- __to_data__: This is a reference path to a JSON string that needs to be converted. The reference path uses the
  Tracardi dot notation for accessing data in the workflow's internal state.

Example: **profile@stats.counters.boughtProducts** would be a valid reference path in some workflows.

# JSON Configuration

Below is an example of the required JSON configuration for this plugin:

```json
{
  "to_data": "profile@stats.counters.boughtProducts"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

An error might occur when the plugin is incapable of parsing the specified JSON string. This usually happens if the JSON
string is malformed or not a valid JSON. In such a case, the following error will be returned:

"JSONDecodeError - Expecting property name enclosed in double quotes"

In the event of such error, the plugin will return the original payload on the "error" port rather than the converted
data.