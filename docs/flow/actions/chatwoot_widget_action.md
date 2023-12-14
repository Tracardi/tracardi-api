# Chatwoot widget

The Chatwoot widget plugin is a user experience (UX) enhancement tool for webpages, integrating Chatwoot's live chat
widget. It allows users to interact with customer support or sales teams directly from the webpage it's implemented on.

# Version

0.7.3

## Description

This plugin integrates a Chatwoot live chat widget into a webpage. The widget is powered by a user-provided Chatwoot
token, which is essential for the widget's functionality. Once set up, the plugin injects a script into the webpage that
initializes and displays the Chatwoot widget, allowing website visitors to start conversations. The widget enhances user
engagement by providing a direct communication channel with the service team.

# Inputs and Outputs

- __Inputs__: The plugin takes a payload object, which serves as a container for passing data.
- __Outputs__:
    - __response__: Outputs the same payload received as input, as this plugin primarily works by adding a UX element to
      the webpage.
    - __error__: Outputs in case of any execution error.

# Configuration

- __Token__: Your Chatwoot token. This is a mandatory field. To find your token, log into chatwoot.com, go to
  settings/inboxes, and look for the JavaScript configuration section.

# JSON Configuration

Example configuration:

```json
{
  "token": "your-chatwoot-token-here"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

Plugins like the Chatwoot widget, which fall under the "UIX Widgets" category, require a synchronous event. It will not
work if sent event is asynchronous.

# Errors

- "Token can not be empty.": This error occurs when the Chatwoot token field is left empty during configuration. The
  token is essential for the widget to function, and thus it must be provided.
- Generic errors related to script injection or execution failures might occur. These are less common and usually
  pertain to issues with the webpage where the script is being injected or network-related problems.