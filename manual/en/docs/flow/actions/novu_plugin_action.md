# Novu trigger plugin

This plugin trigger Novu API and allow to send incoming payload to specified e-mail address.

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