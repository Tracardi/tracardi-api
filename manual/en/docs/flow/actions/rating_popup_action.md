# Show rating widget plugin

This plugin shows the rating widget to user. Rating widget allows user to rate something
at scale from 1 to 5. Widget sends back an event with property **event@properties.rating** 
containing an integer from 1 to 5, according to user rating.

## Input
This plugin takes any payload as input.

## Output
This plugin returns given payload on port **payload** without any changes.

## Plugin configuration

#### With form
- UIX source - provide a URL of API where this widget is located.
  Usually, it's just Tracardi API URL.
- API URL - provide a URL of API to send event back to.
- Title - provide a title for your rating popup. This field does not support dotted notation.
- Popup message - provide a template of message for your rating popup. This field supports dot templates.
- Horizontal position - select a horizontal position for your rating popup.
- Vertical position - select a vertical position for your rating popup.
- Event type - type in a type of event that will be sent back from popup.
- Save event - determine whether sent event should be saved or not. ON - save, OFF - do not save.
- Popup lifetime - define a number of seconds for rating popup to be displayed. After this
  number of seconds, it will disappear without any user interaction.
- Dark theme - you can enable dark theme for your popup. ON - dark mode, OFF - bright mode.

#### Advanced configuration
```json
{
  "api_url": "<url-of-api-for-event-to-be-sent-to>",
  "uix_source": "<url-of-uix-source>",
  "title": "<popup-title>",
  "message": "<popup-message>",
  "lifetime": "<number-of-seconds-to-display>",
  "horizontal_position": " left | center | right ",
  "vertical_position": " top | bottom ",
  "event_type": "<type-of-event-to-be-sent-back>",
  "save_event": "<bool>",
  "dark_theme": "<bool>"
}
```
