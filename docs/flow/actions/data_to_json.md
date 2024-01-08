# Data to JSON

This plugin allows conversion of data objects into a JSON string.

# Version

0.6.0.1

## Description

The Data to JSON plugin takes the data from the payload's input port (which is in dictionary format), then using a
provided reference path, it serializes the data into a JSON string. The processing takes place in the **run** method of
the plugin.

First, the payload is passed to the **run** method. Here, the plugin uses the **get_dot_accessor** method to access the data
referenced by the path provided in the configuration. This path enables the plugin to reach into the payload's nested
structure and find the needed values.

Afterward, the found data is serialized into a JSON string. This process converts
dictionary data into a string format that is easily readable and transferable.

The JSON string is then returned, ready to be passed to the next plugin in the workflow.

# Inputs and Outputs

This plugin has a single input port - **"payload"**, and a single output port - **"payload"**.

The input port accepts a payload object that contains the data to be passed to the plugin.

The output of the plugin is a JSON string of the data referenced by the given path in the payload.

# Configuration

The configuration for this plugin has one parameter:

- **"to_json"**: It's the reference path to data that will be processed by this plugin. This path should be a string in
  dot notation, which represents the location of the desired data in the workflow's internal state. The plugin then
  follows this path to find the data to be serialized into JSON. For example, if we
  have **to_json = "profile@stats.counters.boughtProducts"**, the plugin will access the **boughtProducts** properties under
  the **counters** object in the **stats** object of the **profile**.

# JSON Configuration

Below is an example of a configuration for the Data to JSON plugin:

```json
{
  "to_json": "event@some.path.to.value"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

No predefined errors are emitted by this plugin. If an error occurs, it will be due to issues with loading the payload,
accessing the data on the given path, or converting the data into a JSON string.