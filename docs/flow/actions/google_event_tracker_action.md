# Google Analytics Event Tracker

The Google Analytics Event Tracker is a plugin designed to send custom events to Google Analytics for tracking user
interactions with your website. This documentation will provide an overview of this plugin, including its functionality,
configuration, input/output, and potential errors.

## Version

This documentation is created for plugin version 0.7.3.

## Description

The Google Analytics Event Tracker plugin allows you to send custom event tracking data to Google Analytics. It can be
useful for tracking specific user interactions on your website, such as button clicks, form submissions, or other custom
events. By configuring this plugin, you can define the category, action, label, and value associated with the event you
want to track.

## Inputs and Outputs

- **Input**: This plugin accepts a payload object, typically containing data related to the event you want to track.

- **Outputs**:
    - __response__: This port returns the response status and content if the tracking request was successful.
    - __error__: If the tracking request fails, this port returns an error message.

## Configuration

The Google Analytics Event Tracker plugin requires the following configuration parameters:

- **Google Universal Analytics Tracking ID (source)**: Select the Google Universal Analytics resource that you want to
  use for tracking. The credentials from the selected resource will be used to authorize your account.

- **Event Category (category)**: Define the category of the event you're tracking. The category helps organize events
  into groups. For example, you might use "Buttons" as a category.

- **Event Action (action)**: Specify the action of the event you're tracking. The action describes what a visitor did.
  For example, "Click" could be an action.

- **Event Label (label)**: Enter the name of the event you're tracking. The label provides additional information about
  the event. For instance, "Sign up (a CTA on your button)" might be used as a label.

- **Event Value (value)**: Assign a numeric value to the event you're tracking. The value parameter is optional. Use it
  if the event has a monetary value. For example, if a "Sign up" action is worth 5 USD, you can assign a value of 5.

## JSON Configuration

Here is an example of the JSON configuration for this plugin:

```json
{
  "source": {
    "id": "your-source-id",
    "name": "your-source-name"
  },
  "category": "category",
  "action": "action",
  "label": "label",
  "value": 0
}
```

- **source**: Replace __"your-source-id"__ and __"your-source-name"__ with your actual Google Universal Analytics resource
  ID and name.
- **category**: Replace __"category"__ with the category of the event you want to track.
- **action**: Replace __"action"__ with the action of the event.
- **label**: Replace __"label"__ with the label for the event.
- **value**: Replace __0__ with the numeric value for the event (optional).

## Required Resources

This plugin requires access to a Google Universal Analytics resource. You need to configure the resource, including its
credentials, in the Tracardi admin panel.

## Errors

Possible errors that may occur while using the Google Analytics Event Tracker plugin include:

- If the "Category" field is left empty, an error will occur, indicating that the category cannot be empty.

- If the "Action" field is left empty, an error will occur, indicating that the action cannot be empty.

- If the tracking request fails for any reason, an error message will be returned on the "error" output port.

Please ensure that the required configuration parameters are correctly set to avoid errors during plugin execution.