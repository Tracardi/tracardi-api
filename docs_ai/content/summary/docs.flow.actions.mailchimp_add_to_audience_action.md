This plugin is designed to add contacts to a MailChimp audience based on provided data. Before using this plugin, users
must create a MailChimp account, generate a marketing API key, and add MailChimp to resources. The plugin takes a
payload, which is any JSON-like object, and returns a MailChimp API response on the response port if the action was
successful, or an error from the MailChimp API on the error port if one occurs.

The plugin has several configurable form fields, including the MailChimp resource, the ID of the list (audience), the
contact's email address, the MailChimp merge fields, whether the contact is subscribed, and whether the plugin is
allowed to update existing data. Additionally, users can configure the plugin with a JSON object, which includes the
source ID and name, the list ID, the email address, the merge fields, whether the contact is subscribed, and whether the
plugin is allowed to update existing data.

To find the audience ID, users must click Audience, All contacts, select the Current audience drop-down, choose the
Audience name and defaults in the Setting's drop-down, and then find the Audience ID section.