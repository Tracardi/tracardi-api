# Add contact to Elastic Email plugin

This plugin adds new contact to Elastic Email, based on provided data.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from Elastic Email API on port **response**, or optional error info on port **error** if one
occurs.

## Plugin configuration

#### Form fields

- Elastic Email resource - please select your Elastic Email resource. It should contain:
- Elastic Email Client api key
- Email address - please type in the path to the email address you want the status changed.
- Status - Please put the NUMBER for the status you want. 2=Unsubscribe  https://elasticemail.com/developers/api-documentation/web-api-v2#classes_ContactStatus


#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-elastic-email-resource>",
    "name": "<name-of-your-elastic-email-resource>"
  },
  "email": "<path-to-email-of-new-contact>",
  "status": 2
}
```