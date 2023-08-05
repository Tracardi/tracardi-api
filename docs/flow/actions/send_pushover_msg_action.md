# Pushover push

Connects to Pushover app and pushes a message.

# Version

Version 0.7.1

## Description

The Pushover push plugin allows you to send a message to the Pushover service. It connects to the Pushover API and sends
the specified message to the specified user. The plugin requires Pushover API credentials, including the API token and
user key, which you can obtain by registering at https://pushover.net.

# Inputs and Outputs

## Inputs

This plugin does not take any input.

## Outputs

- **payload**: Returns the response from the Pushover API, including the status and request information.
- **error**: Gets triggered if an error occurs while connecting to the Pushover API.

Example output from the **payload** port:

```json
{
  "status": 200,
  "response": {
    "status": 1,
    "request": "c759f16e-c10a-4066-b91d-05fd06504790"
  }
}
```

# Configuration

The Pushover push plugin requires the following configuration:

- **Resource**: Select or configure a resource that holds the Pushover API credentials. This resource should contain the
  following information:
    - **token**: The API token obtained from Pushover.
    - **user**: The user key obtained from Pushover.

- **Message**: Enter the message to be sent. The message can be a template that uses placeholders for data from the
  profile. For example, if you want to include the name from the profile, you can use the
  placeholder `{{profile@traits.private.pii.name}}`.

# JSON Configuration

Example JSON configuration for the Pushover push plugin:

```json
{
  "source": {
    "name": "pushover",
    "id": "<resource-id>"
  },
  "message": "Hello {{profile@traits.private.pii.name}}!"
}
```

# Required resources

This plugin requires a resource to be configured that holds the Pushover API credentials.

# Errors

The following errors may occur:

- **Could not connect to Pushover API**: This error occurs when the plugin is unable to connect to the Pushover API. The
  error response includes the status code and the response from the API.