# Add points in Mautic plugin

This plugin adds points to given contact, based on provided contact ID.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns payload on port **success** if the action was successful, or additional error info on port **error**
if one occurs.

## Plugin configuration

#### Form fields

- Mautic resource - select you Mautic resource, containing private and public key with API URL.
- Contact ID - type in the path to the field containing contact's ID.
- Number of points - type in the number of points that you want to add to given contact.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-mautic-resource>",
    "name": "<name-of-your-mautic-resource>"
  },
  "contact_id": "<path-to-id-of-the-contact>",
  "points": "<number-of-points-to-add-as-string>"
}
```