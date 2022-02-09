# Add to segment in Mautic plugin

This plugin adds given contact to defined segment in Mautic.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns given payload on port **success** if everything went OK,
or some additional error info on port **error** if an error occurs.

## Plugin configuration

#### With form
- Mautic resource - select your Mautic resource, containing private and public key.
- Contact ID - type in the path to the field containing ID of the Mautic contact.
- Add to segment - type in the ID of the segment that you want to add the given contact to.

#### Advanced configuration
```json
{
  "source": {
    "id": "<id-of-your-mautic-resource>",
    "name": "<name-of-your-mautic-resource>"
  },
  "contact_id": "<path-to-id-of-the-contact>",
  "add_to": "<id-of-the-segment>"
}
```