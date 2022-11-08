# Add contact to Mautic plugin

This plugin adds new contact to Mautic, based on provided data.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from Mautic API on port **response**, or optional error info on port **error** if one
occurs.

## Plugin configuration

#### Form fields

- Mautic resource - please select your Mautic resource. It should contain:
    - Mautic API URL
    - Mautic Client private key
    - Mautic Client public key
- Email address - please type in the path to the email address of your new contact.
- Additional fields - you can add optional mapping for your contact, for example **lastname:
  profile@traits.public.surname**. Remember to use field aliases from Mautic.
- Overwrite with blank - you can overwrite the fields that are not mentioned in configuration, with empty values. ON -
  overwrite with empty, OFF - do not do so.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-mautic-resource>",
    "name": "<name-of-your-mautic-resource>"
  },
  "email": "<path-to-email-of-new-contact>",
  "additional_mapping": {
    "country": "<path-to-country-data>",
    "firstname": "<path-to-first-name>",
    "...": "..."
  },
  "overwrite_with_blank": "<bool>"
}
```