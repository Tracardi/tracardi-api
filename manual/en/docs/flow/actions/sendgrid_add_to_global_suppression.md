# Add contact to Sendgrid plugin

This plugin adds new contact to Sendgrid, based on provided data.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from Sendgrid API on port **response**, or optional error info on port **error** if one
occurs.

## Plugin configuration

#### Form fields

- Token resource - please select your Token resource. It should contain:
- Sendgrid Client api key
- Email address - please type in the path to the email address you want the status changed.


#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-token-resource>",
    "name": "<name-of-your-token-resource>"
  },
  "email": "<path-to-email-of-contact>",
}
```