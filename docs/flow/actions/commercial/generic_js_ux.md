# Generic UIX Plugin

The Generic UIX Plugin is a Tracardi plugin that allows you to display a custom JavaScript widget in your workflow. It
is designed to integrate external JavaScript code into Tracardi and extend its functionality.

## Version

This documentation is based on version 0.8.1 of the Generic UIX Plugin.

## Description

The Generic UIX Plugin enables you to embed custom JavaScript widgets within your Tracardi workflow. It takes the
payload as input, processes it, and displays the custom widget based on the provided configuration. The plugin adds
a `<div>` element with the specified properties to the user interface and injects the JavaScript code by appending
a `<script>` element with the source URL.

# Inputs and Outputs

The Generic UIX Plugin has the following input and output:

**Input**: payload (dict)

- This port accepts a payload object.

**Output**: payload (dict)

- The plugin returns the same payload object.

# Configuration

The Generic UIX Plugin has the following configuration parameters:

- **JavaScript source**: Specify the URL of the JavaScript source code for the custom widget. This URL should point to
  the location where the JavaScript file is hosted.

- **Widget props**: Specify properties as key-value pairs for the widget. You can reference the values using dot
  notation, which allows you to access data from the internal state of the workflow.

```json
{
  "uix_source": "<url-of-uix-source-code>",
  "props": {
    "<props_mapping>": "..."
  }
}
```

# JSON Configuration

Here is an example of the JSON configuration for the Generic UIX Plugin:

```json
{
  "uix_source": "https://example.com/custom-widget.js",
  "props": {
    "color": "red",
    "size": 12,
    "text": "@payload.path.to.data"
  }
}
```

# Required Resources

This plugin does not require external resources to be configured.

# Errors

This plugin does not raise any exceptions or errors.