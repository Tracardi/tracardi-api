# Novu trigger plugin

Novu is an open-source notification infrastructure built for the engineering teams to help them build rich product
notification experiences from single platform.

This plugin triggers Novu API and allows sending incoming messages to services defined within Novu service.

# JSON Configuration

Example:

```json
{
  "source": {
    "id": "0ad150a3-5faa-4161-82b6-5ecfda7eaf6f",
    "name": "api_key"
  },
  "template_name": "template_name",
  "subscriber_id": "profile@id",
  "recipient_email": "profile@pii.email",
  "payload": "{}"
}
```

## Resource configuration

To run this plugin you must provide APIKEY from your Novu profile configuration.

Example of source configuration for Novu trigger:

```json
{
  "token": "token"
}
```