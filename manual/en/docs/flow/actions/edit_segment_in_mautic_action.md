# Edit segment in Mautic plugin

This plugin removes or adds given contact to defined segment in Mautic.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns given payload on port **success** if everything went OK,
or some additional error info on port **error** if an error occurs.

## Plugin configuration

#### Form fields

- Mautic resource - select your Mautic resource, containing private and public key.
- Action - define if you want to add or remove given contact from the given segment.
- Contact ID - type in the path to the field containing ID of the Mautic contact.
- Segment - type in the ID of the segment that you want to add or remove given contact from.

#### Advanced configuration

```json
{
  "source": {
    "id": "<id-of-your-mautic-resource>",
    "name": "<name-of-your-mautic-resource>"
  },
  "action": "add | remove",
  "contact_id": "<path-to-id-of-the-contact>",
  "segment": "<id-of-the-segment>"
}
```