# Does tracardi integrate with Mailchimp?

Yes, Tracardi offers two plugins for sending emails to MailChimp:

- **Send transactional e-mail plugin**: This plugin utilizes the MailChimp Mandrill API to deliver transactional emails.
  It requires a Mandrill account with an API key and proper domain configuration in MailChimp settings. The plugin
  accepts any payload as input and returns a response from the MailChimp API. Depending on the response, it triggers
  either the payload port (for successful delivery) or the error port (for failed delivery).

- **Add to MailChimp audience plugin**: This plugin integrates with the MailChimp API to add contacts to a specified
  audience. It requires a MailChimp account with a marketing API key and a pre-created MailChimp audience. The plugin
  accepts a JSON-like payload as input and returns the MailChimp API response. Upon successful addition of a contact,
  the response is sent to the response port; otherwise, an error message is routed to the error port.
