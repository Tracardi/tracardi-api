# Zapier webhook

This plugin is designed to send messages to a Zapier webhook, which is a way for different apps and services to
communicate with Zapier.

# Version

0.7.0

## Description

When you use this plugin, it performs the action of sending a JSON-formatted message to a specified Zapier webhook URL.
Here's a step-by-step breakdown of what the plugin does:

1. It takes a message, which you need to provide in JSON format.
2. It sends this message to the Zapier webhook URL that you have configured.
3. If the message is successfully received by Zapier, the plugin will consider the action successful and provide you
   with a response indicating that success.
4. In case something goes wrong, like a timeout or connectivity issue, it will give you an error message.

An example of what you might receive if everything works as expected:

```json
{
  "status": 200,
  "json": {
    "some-key": "some-value",
    "...": "..."
  }
}
```

# Inputs and Outputs

The plugin takes in a payload, which is the JSON message you want to send to Zapier. The payload should be formatted as
a JSON object.

The plugin can output through two ports:

- __response__: If the message is sent successfully, the output will be a JSON object that contains the status of the
  request and the JSON response from Zapier.
- __error__: If there is an error in sending the message, like a connection issue or a timeout, the output will be an
  error message.

This plugin does not start the workflow. It is an action to be taken at some point after the workflow has started.

# Configuration

- __URL__: The webhook URL provided by Zapier where the message will be sent.
- __Timeout__: A time limit in seconds for the webhook call. If the call takes longer, the plugin will time out.
- __Body__: The JSON-formatted message you want to send to Zapier. This needs to be valid JSON.

# JSON Configuration

Here's an example configuration for this plugin:

```json
{
  "url": "https://hooks.zapier.com/hooks/catch/10523213728/b4basesz/",
  "timeout": 30,
  "body": "{\"message\":\"Hello, Zapier!\"}"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- __Connection to Zapier webhook failed__: This error occurs if the plugin cannot connect to the specified Zapier
  webhook URL. It could be due to network issues, a wrong URL, or Zapier service downtime.
- __Zapier webhook timed out__: This message appears if the plugin does not receive a response from the Zapier webhook
  within the specified timeout period.
- __<Error Message from JSONDecodeError>__: If the body of the message is not correctly formatted as JSON, you will
  receive an error with the message detailing what went wrong while decoding the JSON.