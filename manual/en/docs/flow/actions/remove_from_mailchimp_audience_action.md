# Remove from MailChimp audience plugin

This plugin removes contact from your MailChimp audience based on provided data.

## Requirements

Before using this plugin, you need to create MailChimp account, generate marketing API key and add MailChimp to
resources.

## Input

This plugin takes payload - any JSON-like object.

## Outputs

Plugin returns MailChimp API response on **response** port if action was successful, or an error from MailChimp API on
port **error** if one occurs.

## Config

#### Config with form

- MailChimp resource - here select your MailChimp marketing resource with API key.
- ID of your list (audience) - it's your audience's ID, that you can easily check on MailChimp website.
- Contact's email address - that's path to email address of your contact. Notice that field can contain multiple values,
  therefore if profile after merging has two email addresses, then plugin will add two contacts to your audience.
- Permanently delete contact - Here you can determine whether given contact should be archived (such that you can re-add
  them)
  or permanently deleted, with no way of recreating and no data left (at least without their consent).

!!! danger "Possible lose of data"

    Removing an email from the recipient list with the delete option has serious ramifications. 
    Once deleted, an e-mail cannot be added without the consent of its owner again. Use the delete 
    option with caution. In most cases, delete: false is the correct configuration


#### Config with JSON


!!! example 

    ```
    {
      "source": {
        "id": "<id-of-your-mailchimp-source>",
        "name": "<name-of-your-mailchimp-source>"
      },
      "list_id": "<id-of-your-audience>",
      "email": "<path-to-field-containing-emails>",
      "delete": <bool>
    }
    ```

