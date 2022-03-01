# Add company to HubSpot plugin

This plugin adds new contact to HubSpot, based on provided data.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns response from HubSpot API on port **response**, or optional
error info on port **error** if one occurs.

## Plugin configuration

#### With form
- HubSpot resource - please select your HubSpot resource. It should contain: 
    - HubSpot client id
    - HubSpot client secret
- Properties - you can add properties for your contact. Remember to use 
  field aliases from HubSpot.
  
#### JSON configuration

```json
{
  "source": {
    "client_id": "<your-client-id>",
    "client_secret": "<your-client-secret>"
  },
  "properties": [
    {
      "name": "name",
      "value": "<a-company-name>"
    },
    {
      "name": "description",
      "value": "<a-company-description>"
    }
  ]
}
```
