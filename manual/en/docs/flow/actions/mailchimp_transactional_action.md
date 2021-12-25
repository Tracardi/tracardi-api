# Send transactional e-mail plugin

This plugin sends transactional email via MailChimp (Mandrill) API.

## Requirements

You'll need a Mandrill account to use this plugin. Then you'll need to generate API key in **settings -> SMTP & API Info** 
on mandrillapp.com.

MailChimp requires a domain configuration to send e-mails, you'll need to add and configure your domain in MailChimp settings. Please refer to MailChimp documentation for details.

The last thing is your MailChimp plan - if you're on the trial version, you are able to send emails only within your own domain, so if your email is **examplemail@example.com**, then your
domain is simply **example.com** and you can send messages only to emails ending with **example.com**.

To get rid of this restriction, you need a paid plan on MailChimp.

## Input

This plugin takes any payload.

## Output

This plugin returns a response from MailChimp API. Depending on the response result it will trigger ether payload 
port (if the response is successful) or error for if the response indicates that the e-mail was not sent.

## Config

Plugin's configuration requires information about API key, sender email, 
message recipient's email(s), message subject and message content.

```json
{
  "source": {
    "name": "MailChimp Token",
    "id": "4529f2a4-62a2-44b0-9a0b-e8dae1f5f6b0"
  },
  "sender_email": "sender@tracardi.com",
  "message": {
    "recipient": "payload@email",
    "content": {
      "type": "text/html",
      "content": "Message body"
    },
    "subject": "subject"
  }
}
```

#### Mailchimp resource

MailChimp token must be stored in Tracardis resources. Please remember to provide noth test and production API key 
(token) in resource configuration.

MailChimp API Tokens can be found in **settings -> SMTP & API Info** on mandrillapp.com. It is a string with random characters.

#### Sender's e-mail

That's the email that you want to send emails from. It has to end with one of your domains
registered in Mandrill. For instance, if your shop is **exampleshop.com**, 
then you may want to send emails from an address like **office@exampleshop.com**, and then that's the value that you
want to insert into plugin configuration. Please notice that this address __does not__ have to exist.

#### Message recipient's email

This is the destination email or emails. It can be in form of dot path to email address (for example **profile@pii.email**). 
You can also insert the address itself. Please notice that merged profiles can have multiple values in one field - 
if John Doe has two or more email addresses in his profile, then plugin will send the message to all of them.

#### Message subject

That's message subject, if you type in **payment**, then recipient of the message will see 
**payment** as the subject of received message.

#### Message content

You can select if your content should be HTML or just plain text. 
You can also use templates for your emails - both in HTML and text format. 

Examples:

##### Example 1 - plain text

```text
Hello {{profile@pii.name}}, your order will be dispatched in next two days.
```

This message will have the **{{profile@pii.name}}** changed to the current profile's name, so John Doe will
see **'Hello John, your order will be dispatched in next two days.'** in his message.

##### Example 2 - HTML

```html
<h1>Hello {{profile@pii.name}}!</h1>
<p>Thanks for visiting our website on {{profile@metadata.time.lastVisit}}!</p>
<p style="color:red">To thank you, we send you a photo of cute dog. Enjoy:</p>
<img src="<url-to-photo-of-cute-dog>"/>
```
Like before, recipient will see his name in the header, and the text with date of his last visit,
together with the red text about a photo of a dog, and a photo itself.

## Tip

On MailChimp site, you can turn on the test mode after clicking on you username in up-right corner.
In the test mode, you can generate test API key. You can use it in Tracardi for test purposes - 
messages won't be sent, but MailChimp will act like they are, so you can test your
configuration without being charged a single cent.




