# Show contact popup plugin

This plugin shows the contact widget to user. This widget allows user to give you some contact data (phone number or
email address), which will be sent back in Tracardi event.
(**event@properties.contact**)

## Input

This plugin takes any payload as input.

## Output

This plugin returns given payload on port **payload** without any changes.

## Plugin configuration

#### Form fields description

- UIX source - provide a URL of API where this widget is located. Usually, it's just Tracardi API URL.
- API URL - provide a URL of API to send event back to.
- Popup message - provide a template of message for your contact popup. This field supports dot templates.
- Contact data type - define whether you want the user to provide their email address or phone number.
- Horizontal position - select a horizontal position for your contact popup.
- Vertical position - select a vertical position for your contact popup.
- Event type - type in a type of event that will be sent back from popup.
- Save event - determine whether sent event should be saved or not. ON - save, OFF - do not save.
- Dark theme - you can enable dark theme for your popup. ON - dark mode, OFF - bright mode.

#### Advanced configuration

```json
{
  "uix_source": "<url-of-uix-source>",
  "api_url": "<url-of-api-for-event-to-be-sent-to>",
  "content": "<popup-message>",
  "contact_type": "email | phone",
  "horizontal_pos": " left | center | right ",
  "vertical_pos": " top | bottom ",
  "event_type": "<type-of-event-to-be-sent-back>",
  "save_event": "<bool>",
  "dark_theme": "<bool>"
}
```
