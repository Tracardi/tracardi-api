# Cut out data

This plugin is designed to extract a part of referenced data and return it as the payload. 

## Version

This documentation was created for the plugin version 0.8.0.

## Description

The Cut Out Data plugin enables the user to specify a path to a property within the workflow's internal data. This could be in the event, profile, memory, or other data. The plugin then extracts this data and returns it as the payload. 

It is also possible for the returned data to be wrapped within an object with a specified key. If a key is provided in the configuration, the data at the specified path will be returned as an object where the key is the provided key and the value is the extracted data.

For example, if the key is "myKey" and the extracted data is "myData", then the returned object would be:

```json 
{
  "myKey": "myData"
}
```

If no key is provided, the plugin just returns the extracted data, whatever it may be.

## Inputs and Outputs

This placeholder accepts any JSON-like object as its input. 

The output is given below:

```json 
{
  "<optional key>": "<output>"
}
```
Where the optional key is the value provided in the configuration (if any), and output is the piece of data that was specified by the path in the configuration. 

Also, note that this plugin cannot start a workflow. It needs to have an input passed onto it.

## Configuration

The plugin has two configuration parameters:

- Path to data: This field allows you to specify the path to the internal data you are interested in. Generally, it should be in the form of __<data_type>@<path.to.property>__. E.g. "event@session.context.browser.browser.userAgent".

- Return as: This is an optional field that, when filled, would wrap the extracted data in an object with the provided key.

## JSON Configuration

Here's an example of the configuration:

```json
{"trait": "event@session.context.browser.browser.userAgent", "key": "userAgent"}
```

This configuration would result in an output where the user agent of the browser is returned as an object with the key userAgent.

## Required resources
This plugin does not require external resources to be configured.

## Errors

- If the "Path to data" configuration is left empty, you will receive a __Trait should not be empty__ error. This error occurs when the configuration does not contain a path to any data in the workflow's internal state.
    
- If the "Return as" configuration is left empty or is filled with whitespace, you will receive a __Key is empty__ error.
  
These errors can halt the processing of the plugin, so it is important to rectify them for the workflow to proceed.