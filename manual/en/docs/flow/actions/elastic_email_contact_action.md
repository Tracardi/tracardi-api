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
- Email address - please type in the path to the email address of your new contact.
- Additional fields - you can add optional mapping for your contact, for example **lastname:
  profile@traits.public.last_name**. Remember to use field aliases from Elastic Email.
- Overwrite with blank - you can overwrite the fields that are not mentioned in configuration, with empty values. ON -
  overwrite with empty, OFF - do not do so.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-elastic-email-resource>",
    "name": "<name-of-your-elastic-email-resource>"
  },
  "email": "<path-to-email-of-new-contact>",
  "additional_mapping": {
    "country": "<path-to-country-data>",
    "firstname": "<path-to-first-name>",
    "...": "..."
  },
}
```