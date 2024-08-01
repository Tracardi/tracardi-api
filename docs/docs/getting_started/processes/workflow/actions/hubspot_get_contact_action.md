# Get contact from HubSpot plugin

This plugin gets a contact from HubSpot, based on provided data.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns response from HubSpot API on port **response**, or optional
error info on port **error** if one occurs.

## HubSpot app
Firstly, you need to [create an app](https://developers.hubspot.com/docs/api/private-apps#create-a-private-app) in 
a HubSpot account.

### Initiating  connection
You need your apikey/accesstoken 
Below there is a path from main page to this:

hubspot.com -> login -> choose your account -> settings -> account setup -> integrations -> private app

  
* scopes: for getting contact, you need to choose crm.schemas.contacts.read scope, but this match only with this 
  and Add Contact to HubSpot plugin. For other plugins connecting to HubSpot, you should choose other scopes.   
  We recommend choose all the following scopes: 
  
        crm.objects.companies.write, crm.objects.companies.read, crm.objects.contacts.write, crm.schemas.contacts.read, content

You can now access the access token for this app


## Plugin configuration

#### With form
* HubSpot resource - please select your HubSpot resource. It should contain: 
    * access token - how you access the site. Like any api token
     
* contact id - id of a contact you want to get.

#### JSON configuration - example

```json
{
  "source": {
    "access_token": "<your-access-token-optionally>",
  },
  "contact_id": "<your-contact-id>"
}
```
