# Fetch Mautic contact by ID plugin

This plugin fetches a contact from Mautic, based on provided contact ID.

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
- Contact ID - please type in the path to ID of the contact that you want to fetch.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-mautic-resource>",
    "name": "<name-of-your-mautic-resource>"
  },
  "contact_id": "<path-to-contact-id>"
}
```