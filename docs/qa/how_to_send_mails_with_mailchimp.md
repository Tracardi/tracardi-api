To send emails with Mailchimp in Tracardi, follow these steps:

* __Obtain the API key__: Log in to your Mailchimp account, click on your account icon in the top-right corner,
  select "Profile," then choose "Extras > API keys." Click on "Create A Key" to generate an API key. Copy this key to
  the Token field in the Tracardi form.

* __Verify the API key__: If you encounter an error stating that the API key is invalid, double-check that you have set the
  correct API key from Mailchimp.
* __Check API key configuration__: Make sure you have followed the tutorial for finding and setting the API key correctly.
  The API key should match the one generated in your Mailchimp account.

* __Save API key__: If you are unable to change the API key and it does not get saved, try disabling the resource and then
  enabling it again. This may help in saving the updated API key.

* __Troubleshooting__: If the issue persists, reach out to the plugin developer or support team to investigate the error and
  find a solution.

Additionally, as an alternative solution, you can consider using the SMTP mailer in Tracardi to send emails. This can be
helpful if you continue to encounter difficulties with the Mailchimp integration.

## How to send email only once

Regarding triggering emails only once for the same event and user, you can achieve this by saving information about the
sent email in the user's profile. For example, after sending an email, use the "Copy Data" action in Tracardi to set a
flag in the profile (e.g., profile@aux.sent_email = 1). Before triggering the email, you can check this flag to determine
if the email has already been sent for a specific event.

Remember, it's important to save and utilize the necessary information in the profile to conditionally send emails and
avoid duplicate sends based on specific events or user actions.

If you need further assistance, don't hesitate to seek help from Tracardi support or consult with the Tracardi
community.