# Fetch contact from ActiveCampaign plugin

This plugin fetches ActiveCampaign contact based on given email address.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns contact data on port **result** if the contact was found,
or error info on port **error** if an error occurred or the contact was not found.

## Configuration
```json
{
  "source": {
    "id": "<id-of-your-activecampaign-resource>",
    "name": "<name-of-your-activecampaign-resource>"
  },
  "email": "<path-to-email-address>"
}
```