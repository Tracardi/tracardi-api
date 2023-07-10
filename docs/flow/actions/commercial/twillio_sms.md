# Send SMS

The "Send SMS" plugin in Tracardi enables you to send SMS messages using the Twilio gateway. With this plugin, you can
integrate SMS messaging functionality into your Tracardi workflows.

## Description

The "Send SMS" plugin allows you to send SMS messages to a specified phone number using the Twilio gateway. You can
customize the sender's phone number, the recipient's phone number, and the message content. The plugin uses the Twilio
API to send the SMS messages.

## Inputs and Outputs

- **Input**: This plugin accepts any payload as input.

- **Output Ports**:
    - **result**: This port returns the result of the SMS sending operation, including details such as the status of the
      message, price, direction, and more.
    - **error**: This port is triggered if an error occurs during the execution of the plugin.

## Configuration

The "Send SMS" plugin has the following configuration options:

- **Twilio Resource**: Select the Twilio resource to use for sending SMS messages. You can choose an existing Twilio
  resource from the available options.

- **From phone number**: Specify the phone number from which you want to send the SMS. You can use dot notation to
  reference the phone number from the payload.

- **To phone number**: Specify the phone number to which you want to send the SMS. You can use dot notation to reference
  the phone number from the payload.

- **SMS Message**: Enter the content of the SMS message that you want to send. You can include placeholders in the
  message using double curly braces ({{ }}) and referencing data from the payload. For example, you can reference the
  product ID using `{{event@properties.product_id}}`.

## Example Usage

Here's an example of how the "Send SMS" plugin can be used:

```yaml
- send_sms:
    resource:
      name: "My Twilio Resource"
      id: "12345678"
    from_number: "event@properties.sender_number"
    to_number: "event@properties.recipient_number"
    message: "Your order {{event@properties.order_id}} has been shipped. Thank you!"
```

In this example, the plugin is configured to send an SMS using the Twilio resource with the name "My Twilio Resource"
and ID "12345678". The sender's phone number is retrieved from the payload using the dot
notation `event@properties.sender_number`. The recipient's phone number is also retrieved from the payload
using `event@properties.recipient_number`. The message content includes the order ID from the payload
using `{{event@properties.order_id}}`.

Please note that the above example assumes that the necessary data is available in the payload. Make sure to adjust the
dot notation and payload structure according to your specific use case.

