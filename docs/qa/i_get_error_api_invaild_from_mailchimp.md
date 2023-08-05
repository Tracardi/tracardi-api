# I get error API Invalid from Mailchimp

If you are receiving an "API Invalid" error from Mailchimp, it usually indicates that the API key you provided is
incorrect or invalid. Here is a step-by-step guide to obtaining the correct API keys for Mailchimp:

* Log in to your Mailchimp account.
* Click on your account icon in the top-right corner.
* Select "Profile".
* In the "Profile" section, choose "Extras" and then "API keys".
* To add email addresses to a Mailchimp audience, you need the Mailchimp API key. Click on "Create A Key" under the "Your API keys" section and generate a new API key.
* To send one-to-one transactional emails, you need the Mandrill API key. Click on "Add a Mandrill API Key" and follow the instructions. Note that you will need to verify your domain with Mandrill to send one-to-one emails.
* Once you have generated the API keys, copy the respective key (Mailchimp API or Mandrill API) and paste it into the Token field in the Tracardi Form or your Mailchimp integration settings in Tracardi.

For more information on generating, disabling, and deleting API keys in Mailchimp, you can refer to the official
Mailchimp documentation at https://mailchimp.com/help/about-api-keys/.

Please keep in mind that sending one-to-one emails using Mandrill requires domain verification. You can find additional
guidance on domain verification and configuring your DNS in the following Mailchimp documentation links:

* [Mandrill Authentication and Delivery - Authentication](https://mailchimp.com/developer/transactional/docs/authentication-delivery/#authentication)
* [Mandrill Authentication and Delivery - Configure Your DNS](https://mailchimp.com/developer/transactional/docs/authentication-delivery/#configure-your-dns)

By following these instructions and ensuring the correct API key is used, you should be able to resolve the "API
Invalid" error and successfully connect Tracardi with Mailchimp.
