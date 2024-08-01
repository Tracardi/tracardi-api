# Plugin documentation

This plugin adds new contact to HubSpot, based on provided data.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from HubSpot API on port **response**, or error info on port **error** if one occurs.

## HubSpot resource

To connect Tracardi with HubSpot you need a HubSpot resource. If you do not have HubSpot resource set, go to Resources
and create a new resource. More details on how to do it you can find in resource tab. If you did not install Hubspot then go to
extensions and install it. It will create both resource and plugins.

### Resource scope

In order to connect to the HubSpot you need a private app. The information on how to create it is provided during
creating the HubSpot resource. If you have resource you most probably have everything set up. There is only one
important information regarding using this plugin. The resource that you create must have the following rights. 
It was set when you created "private app" in hubspot.

```
 crm.objects.contacts.write, 
 crm.schemas.contacts.read
```

# Plugin configuration

Use one of the following forms of configuration. Configuration via FORM or advanced configuration with JSON.

## With form

* HubSpot's resource - please select your HubSpot resource.
* Type contact properties such as: email, firstname, lastname, phone, etc.

## JSON configuration - example

```json
{
  "source": {
    "id": "<resource-id>",
    "name": "<resource-name>"
  },
  "properties": {
    "email": "<a-contact-email>",
    "firstname": "<a-contact-firstname>",
    "lastname": "<a-contact-lastname>"
  }
}
```
