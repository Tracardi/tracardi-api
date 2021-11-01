# Pushover plugin

This plugin sends a message to pushover service.

# Requirements

To use this plugin you must register at https://pushover.net and obtain API_TOKEN and USER_KEY.

# Configuration

THis plugin needs access to resource that will hold the information on PushOver credentials.

## Resource configuration

```json
{
  "token": "<API_TOKEN from PushOver>",
  "user": "<USER_KEY from PushOver>"
}
```

## Plugin configuration

```json
{
  "source": {
    "name": "pushover",
    "id": "<resource-id>"
  },
  "message": "Hello {{profile@traits.private.pii.name}}!"
}
```

Message can be a template that uses placeholders for data from profile. Above you can 
see a simple template that when executed will replace `{{profile@traits.private.pii.name}}`
with name (`traits.private.pii.name`) from profile.

# Input

This plugin does not take any input

# Output

Output returns status and response body from PushOver service.

```json
{
  "status": 200,
  "body": {
    "status": 1,
    "request": "c759f16e-c10a-4066-b91d-05fd06504790"
  }
}
```
