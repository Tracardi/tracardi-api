# ClickSend Send SMS

The ClickSend Send SMS plugin allows you to send SMS messages using the ClickSend gateway in your Tracardi workflows. This documentation will provide an overview of the plugin, including its functionality, configuration options, and examples of how to use it.

## Version

This documentation is created for version 0.8.2 of the plugin.

## Description

The ClickSend Send SMS plugin is used to send SMS messages through the ClickSend gateway. You can customize the content of the SMS message and specify the recipient's phone number. This plugin supports dynamic content generation by allowing you to use data placeholders in your SMS message.

### How it Works

1. The plugin takes a payload as input, which is a dictionary containing various data.
2. It retrieves the necessary configuration parameters, including the ClickSend resource, SMS message template, sender, and recipient phone number.
3. The SMS message template can contain placeholders that will be replaced with data from the payload. The placeholders use a dot notation to reference specific data in the payload.
4. The plugin sends the SMS message to the specified recipient using the ClickSend gateway.
5. It captures the response status and content from the ClickSend gateway.

**Example Output**:
```json
{
  "status": 200,
  "content": "SMS message sent successfully."
}
```

# Inputs and Outputs

The ClickSend Send SMS plugin accepts a payload as input and provides two output ports: "response" and "error."

**Inputs**:
- __payload__: This port accepts a payload object, which is a dictionary containing data.

**Outputs**:
- __response__: This port returns the response status and content from the ClickSend gateway if the SMS message is sent successfully.
- __error__: This port returns an error if the SMS message sending process fails.

The plugin does not have the capability to start a workflow.

# Configuration

The ClickSend Send SMS plugin has the following configuration parameters:

- __Resource__: Select your ClickSend resource, which defines the credentials for the ClickSend gateway.
- __Message template__: Type the SMS message. This message template can include data placeholders that will be replaced with data from the payload.
- __Sender__: Type the sender's name or leave it blank to use the default sender. Custom sender names can be configured in the ClickSend system.
- __Recipient__: Type or reference the recipient's phone number for the SMS message.

# JSON Configuration

Here's an example JSON configuration for the ClickSend Send SMS plugin:

```json
{
  "resource": {
    "id": "your_resource_id",
    "name": "ClickSend Resource"
  },
  "message": "Hello, {profile@data.pii.firstname}! Your appointment is confirmed for {payload@appointment.date}.",
  "sender": "Tracardi",
  "recipient": "profile@data.contac.telephone"
}
```

# Required Resources

This plugin requires the configuration of a ClickSend resource to work. You need to set up the ClickSend resource with your ClickSend credentials to enable the plugin to send SMS messages.

# Errors

The ClickSend Send SMS plugin may raise the following errors along with their descriptions:

- **HTTP Request Error**: This error may occur if there is an issue with the HTTP request made to the ClickSend gateway.
- **Invalid Recipient**: If the recipient's phone number is invalid or not provided, this error may occur.
- **Missing Message**: If the message template is empty or not provided, this error may occur.
- **Profile Event Sequencing Error**: This error may occur if the plugin is unable to access profile data. It requires a profile for certain dot notation references.

Please note that these errors may occur based on the specific conditions or configurations of the plugin.