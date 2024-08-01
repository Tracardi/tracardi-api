# Show consent bar

This plugin displays a consent pop-up on the front-end of your application.

# Version

0.8.2

## Description

The **Show consent bar** plugin is used to display a consent bar or pop-up on the front-end of the application. This is
particularly useful when obtaining user consent for specific actions or features as required by regulations such as
GDPR.

The plugin's behavior can be configured based on several parameters in its configuration. The parameters include the
API's endpoint, the location of the micro frontend for the consent bar (usually the location of the Tracardi API), and
details such as the type, height, and position of the widget.

The widget can be placed either at the top or bottom of the page, and its height can be adjusted as per requirements.
There is also an option to enable or disable the widget as needed.

The plugin doesn't manipulate received data. It passes through the plugin unmodified from the input port (labeled *
*payload**) to the output port (also labeled **payload**).

# Inputs and Outputs

The plugin has one input port and one output port.

Inputs:

- **payload**: This port accepts a payload object.

Outputs:

- **payload**: This port returns the input payload object.

# Configuration

The plugin can be configured via the following parameters:

- **endpoint**: This field is required to specify the location
- **uix_source**: This field has the location of the micro frontend for the consent bar. Usually, this is the Tracardi API
  location. Different locations can be specified if using a CDN.
- **event_type**: This field specifies the type of event to be triggered.
- **agree_all_event_type**: This field specifies the type of event to be triggered when all consents are agreed to.
- **position**: This field can be adjusted to place the widget either at the top or the bottom of the application window.
- **expand_height**: This field can be adjusted to specify the height of the expanded widget.
- **enabled**: This field can be set to either true or false to enable or disable the widget respectively.
- **always_display**: If set to true the consent bar will always be displayed regardless if the consents were already given.

# JSON Configuration

Here is an example configuration:

```json
{
  "endpoint": "http://localhost:8686",
  "uix_source": "http://localhost:8686",
  "event_type": "user-consent-pref",
  "agree_all_event_type": "agree-all-event-type",
  "position": "bottom",
  "expand_height": 400,
  "enabled": true,
  "always_display": false
}
```

# Required resources

This plugin does not require any external resources to be configured.

# Errors

- "This field should not be empty": This error occurs when the **endpoint** or **uix_source** field in the configuration is
  left empty.
- "This field should be either [top] or [bottom]": This error occurs when the **position** field in the configuration is
  left empty or contains an invalid value.
- "This field must be a number": This error occurs when the **expand_height** field in the configuration contains a
  non-numeric value.