# Add to MailChimp audience plugin
This plugin adds contact to your MailChimp audience based on provided data.
## Requirements
Before using this plugin, you need to create MailChimp account, generate marketing API key and 
add MailChimp to resources.
## Input
This plugin takes payload - any JSON-like object.
## Outputs
Plugin returns MailChimp API response on **response** port if action was successful, or
an error from MailChimp API on port **error** if one occurs.
## Config
#### Config with form:
- MailChimp resource - here select your MailChimp marketing resource with API key.
- ID of your list (audience) - it's your audience's ID, that you can easily check on MailChimp website.
- Contact's email address - that's path to email address of your contact. Notice that field can contain multiple values,
so if profile after merging has two email addresses, then plugin will add two contacts to your audience.
- MailChimp merge fields - here you can determine relation between your audience's merge fields and fields in Tracardi data.
If you associate merge field **FNAME** (which is default merge field for first name) with dot path **profile@pii.name**, then your contact's first name will be taken from this Tracardi field.
- Subscribed - this parameter determines whether contact is ready for sending emails or should receive confirmation email from
MailChimp. According to MailChimp's policy, you must have contact's explicit consent in order to mark them as subscribed.
- Update existing data - here you can determine whether plugin is allowed to edit existing contacts according to email address
compatibility.

#### Config with JSON:
```
{
  "source": {
    "id": "<id-of-your-resource>",
    "name": "<name-of-your-resource>"
  },
  "list_id": "<id-of-your-mailchimp-audience>",
  "email": "<dot-path-to-field-containing-email-address>",
  "merge_fields": {
    "<merge_field_name>": "<tracardi-field-name>" 
  },
  "subscribed": <bool>,
  "update": <bool>
}
```


