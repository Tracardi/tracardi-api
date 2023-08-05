# Rating Popup Plugin

This plugin shows the rating widget to user. Rating widget allows user to rate something
at scale from 1 to 5. Widget sends back an event with property **event@properties.rating** 
containing an integer from 1 to 5, according to user rating.

## Description

The Rating Popup Plugin displays a customizable rating widget as a popup. The plugin allows you to configure the title, message, lifetime, positioning, styling, and reporting of the rating event. You can define the API URL to send the event with the rating, specify the event type, and choose whether to save the event or not.

When the plugin is executed, it renders the rating widget with the configured settings. The payload object is passed through the plugin unchanged.

Version: 0.8.1

# Inputs and Outputs

## Inputs

- **payload** (dict): This input port accepts a payload object.

## Outputs

- **payload** (dict): This output port returns the given payload without any changes.

# Configuration

The Rating Popup Plugin supports the following configuration parameters:

- **Widget configuration**
  - **Title**: This text will become the title of your rating popup.
  - **Popup message**: This is the message to be displayed in the rating popup. You can use a template here.
  - **Popup lifetime**: Please provide the number of seconds for the rating popup to be displayed.

- **Positioning**
  - **Horizontal position**: This is the horizontal position of your popup. Choose from "Left", "Center", or "Right".
  - **Vertical position**: This is the vertical position of your popup. Choose from "Top" or "Bottom".

- **Styling**
  - **Pop-up styling**: This field allows you to customize the appearance of the rating popup.
  - **Title size**: This field allows you to set the size of the title.

- **Reporting rating**
  - **API URL**: Provide the URL of the Tracardi instance to send the event with the rating.
  - **Event type**: Please provide the type of event to be sent back after selecting the rating.
  - **Save event**: Determine whether the sent event should be saved or not.

# JSON Configuration

Here is an example of the JSON configuration for the Rating Popup Plugin:

```json
{
    "api_url": "http://localhost:8686",
    "title": "My Rating",
    "message": "Please rate your experience.",
    "lifetime": "10",
    "horizontal_position": "center",
    "vertical_position": "bottom",
    "event_type": "rating",
    "save_event": true,
    "styling": {
        "margin": {
            "left": 0,
            "top": 0,
            "right": 0,
            "bottom": 0
        },
        "padding": {
            "left": 20,
            "top": 20,
            "right": 20,
            "bottom": 20
        },
        "color": {
            "background": "rgba(255,255,255,0.95)",
            "text": "rgba(0,0,0,1)"
        },
        "border": {
            "size": 0,
            "radius": 0,
            "color": "black"
        }
    },
    "title_size": "20"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

This plugin does not generate any errors.