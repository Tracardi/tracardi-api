# Salesforce Data Extension plugin

This plugin creates/ updates a record in Salesforce Marketing Cloud Data Extension, according to given configuration.

## Requirements

In your Marketing Cloud, click on your profile image. Then select **Setup**. On the left, select **Apps** > **Installed
Packages**. There click **New** button. Give some name and description to your package, then click **Add Component**
button. Select **API Integration**, then **Server-to-Server**. Then select
**Data Extensions** > **Write** under **Data** header in scopes configuration and save it. Now you should see:

- Client Id
- Client Secret
- REST Base URI

Paste Client ID and Client Secret while creating new resource, and to find your subdomain, take **https://[THIS-PART]
.rest.marketingcloudapis.com/** from REST Base URI. To use the plugin, you need to provide Data Extension ID. To find
it, go to **Audience Builder** > **Contact Builder**. Then select **Data Extensions** on the top. Then right-click on
your Data Extension's name, and copy the link. Now paste **https:// ... /data-extension/[THIS-PART]/properties/** as
Data Extension ID in plugin configuration form.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns given payload on port **success** if the action was successful, or some additional error information
on port **error** if one occurred.

## Configuration

```json
{
  "source": {
    "id": "<id-of-your-marketing-cloud-resource>",
    "name": "<name-of-your-marketing-cloud-resource>"
  },
  "extension_id": "<id-of-your-data-extension>",
  "update": "<bool-update-existing-records>",
  "mapping": {
    "column1": "profile@id",
    "column2": "event@properties.revenue",
    "...": "..."
  }
}
```


