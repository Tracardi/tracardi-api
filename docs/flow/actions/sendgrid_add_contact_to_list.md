# Send bulk e-mail plugin

This plugin sends bulk email via Sendgrid API.

## Requirements

You'll need a Sendgrid account to use this plugin. Then you'll need to generate API key 

Sendgrid requires a domain configuration to send e-mails, you'll need to add and configure your domain in Sendgrid settings. Please refer to Sendgrid documentation for details.

The last thing is your Sendgrid plan - if you're on the trial version, you are able to send emails only within your own domain, so if your email is **examplemail@example.com**, then your
domain is simply **example.com** and you can send messages only to emails ending with **example.com**.

To get rid of this restriction, you need a paid plan on Sendgrid.

## Input

This plugin takes any payload.

## Output

This plugin returns a response from Sendgrid API. Depending on the response result it will trigger ether payload 
port (if the response is successful) or error for if the response indicates that the e-mail was not sent.

## Config

Plugin's configuration requires information about API key, sender email, 
message recipient's email(s), message subject and message content.

```json
{
  "source": {
    "id": "<id-of-your-sendgrid-resource>",
    "name": "<name-of-your-elastic-email-resource>"
  },
  "email": "<path-to-email-of-new-contact>",
  "list_ids": "<comma-seperated-list-of-list-ids>",
  "additional_mapping": {
    "address_line_1": "<path-to-country-data>",
    "first_name": "<path-to-first-name>",
    "last_name": "<path-to-last-name>",
    "...": "..."
  }
}
```

#### Sendgrid resource

Sendgrid token must be stored in Tracardi's resources. Please remember to provide both test and production API key 
(token) in resource configuration.

Sendgrid API Tokens can be found in **settings -> SMTP & API Info** on  It is a string with random characters.


