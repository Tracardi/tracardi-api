# Add contact to ActiveCampaign action

This plugin adds new contact to ActiveCampaign, or updates existing one if the 
contact already exists.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns created contact's info on port **success** if the action was
successful, or some error info on port **error** if there was an error.

## Configuration
```json
{
  "source": {
    "id": "<id-of-your-activecampaign-resource>",
    "name": "<name-of-your-activecampaign-resource>"
  },
  "fields": {
    "email": "<path-to-email>",
    "lastName": "<path-to-last-name>",
    "...": "..."
  }
}
```