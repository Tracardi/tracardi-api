# Show question popup plugin

This plugin shows a question to user, with two possible answers. The answer click by user will be sent back to tracardi 
as a new event type. User can define the type in __Event type__ field in the configuration form.  

## Input

This plugin takes any payload as input.

## Output 

This plugin returns given payload on port **payload** without any changes.

## Plugin configuration

#### Form fields 

- UIX Source - provide a URL, where UIX elements are located. Usually it's
  **http://localhost:8686** (Tracardi API).
- API URL - question popup sends an event after user has answered given question.
  That's the URL of API that event will be sent to.
- Popup title - provide a title for your popup. This field does not support dotted notation.
- Popup content - provide a content for your popup. This field supports dot template.
- Left button text - provide a text to be displayed on the left button. This field does not support
  dotted notation.
- Right button text - provide a text to be displayed on the right button. This field does not support
  dotted notation.
- Horizontal position - select a horizontal position for your popup to be displayed.
- Vertical position - select a vertical position for your popup to be displayed.
- Event type - type in the type of event to be sent back to given API URL. This field does not support
  dotted notation.
- Save event - you can save the event that is sent back from popup. ON - save, OFF - do not save.
- Popup lifetime - provide a number of seconds for the popup to be displayed. After this amount of
  seconds, the popup will disappear without any user interaction.
- Dark theme - you can switch your popup into dark mode. ON - dark theme, OFF - bright theme.

#### Advanced configuration

```json
{
  "api_url": "<url-of-api-for-event-to-be-sent-to>",
  "uix_source": "<location-of-uix-components-source>",
  "popup_title": "<popup-title>",
  "content": "<message-template>",
  "left_button_text": "<left-button-text>",
  "right_button_text": "<right-button-text>",
  "horizontal_pos": " left | center | right ",
  "vertical_pos": " top | bottom ",
  "event_type": "<type-of-event-to-be-sent-back>",
  "save_event": "<bool>",
  "popup_lifetime": "<integer-as-string>",
  "dark_theme": "<bool>"
}
```