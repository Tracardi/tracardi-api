# Zendesk widget

The Zendesk widget plugin is designed to add a Zendesk chat interface to webpages, enhancing customer interaction and
support.

# Version

0.7.3

## Description

This plugin integrates the Zendesk chat widget into webpages. The widget facilitates customer support and engagement
directly from the website. It requires a specific Zendesk script URL to function. Once configured, the plugin appends a
script tag to the webpage, which activates the Zendesk widget. This addition can significantly enhance the user
experience by providing a direct and convenient communication channel with support or sales teams.

# Inputs and Outputs

- __Inputs__: The plugin takes a payload object. This payload serves as a container for data within the workflow but is
  not directly modified by this plugin.
- __Outputs__:
    - __response__: Outputs the original payload after processing. The main function of this plugin is to append the
      Zendesk widget to the webpage.
    - __error__: Outputs in case of any execution error.

# Configuration

- __Script URL__: The URL of the Zendesk script. This URL is provided when you set up an account with Zendesk. Refer to
  Zendesk's documentation for more details.

# JSON Configuration

Example configuration:

```json
{
  "script_url": "https://static.zdassets.com/ekr/snippet.js?key={your-key}"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

Plugins like the Zendesk widget, which fall under the "UIX Widgets" category, require a synchronous event. It will not
work if sent event is asynchronous.

# Errors

- "Script URL can not be empty.": This error occurs when the script URL for the Zendesk widget is not provided in the
  plugin configuration. The script URL is essential for the widget's operation.
- General script-related errors might occur, typically related to the execution of the appended JavaScript in the
  webpage environment. These could be due to conflicts with other scripts or issues in the webpage's structure.