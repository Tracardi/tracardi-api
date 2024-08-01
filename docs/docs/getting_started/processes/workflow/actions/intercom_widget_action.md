# Intercom widget

The Intercom widget plugin is designed to integrate the Intercom chat system into a webpage, enhancing user interaction
and support.

# Version

0.7.3

## Description

This plugin adds the Intercom messaging widget to a webpage, allowing for real-time chat and support interactions. It
requires an Intercom application ID to function. Once configured, the plugin injects a JavaScript snippet that
initializes the Intercom widget on the webpage. This widget can significantly improve user engagement, providing a
convenient way for visitors to communicate with the website's support or sales teams.

# Inputs and Outputs

- __Inputs__: The plugin takes a payload object as input. This payload is typically used for passing data within the
  workflow but isn't directly modified by this plugin.
- __Outputs__:
    - __response__: Outputs the original payload after processing, as the primary function of this plugin is to append
      the
      Intercom widget to the webpage.
    - __error__: Outputs in case of any execution error.

# Configuration

- __Application ID__: The unique identifier for your Intercom application. This ID is crucial for linking the widget to
  your specific Intercom account.

# How to obtain Application ID

To use this application on your webpage, first, create an account at www.intercom.com.

1. Once you've signed up and set up your initial application in the Intercom dashboard, locate your app_id. You can find
   this in the URL, which looks like this: `https://app.intercom.com/a/apps/{app_id here}`.
2. Then, take this app_id and input it into the plugin's configuration to set it up.

# JSON Configuration

Example configuration:

```json
{
  "app_id": "your-intercom-application-id"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

Plugins like the Intercom widget, which fall under the "UIX Widgets" category, require a synchronous event. It will not
work if sent event is asynchronous.

# Errors

- "Application ID can not be empty.": This error occurs when the application ID for the Intercom widget is not provided.
  The application ID is essential for the widget's operation.
- General script-related errors might occur, typically related to the execution of the appended JavaScript in the
  webpage environment. These could be due to conflicts with other scripts or issues in the webpage's structure.