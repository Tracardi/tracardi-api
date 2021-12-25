# Send transactional e-mail plugin
This plugin sends transactional email via Mailchimp (Mandrill).
## Requirements
You'll need a Mandrill account, you can create one using your Mailchimp account.
Then you'll need to generate API key in ```settings -> SMTP & API Info``` on mandrillapp.com.
To send e-mails, you'll need to add and configure your domain in Mandrill. App's website
is fairly helpful in this case. Last thing is your Mandrill plan - if you're on trial version, you are
able to send emails only within your own domain, so if your email is ```examplemail@example.com```, then your
domain is simply ```example.com``` and you can send messages only to emails ending with ```example.com```.
To get rid of this restriction, you need a paid plan on Mandrill.

## Input
This plugin simply takes payload, so any data in form of type JSON.

## Output
This plugin returns given payload (without any changes) on port ```payload``` and 
list of responses from mailing API (so if messages were sent or not and things like message id) on port ```response```.

## Config
Plugin's configuration requires information about API key, sender email, 
message recipient's email(s), message subject and message content.
#### Mailchimp resource
Here you need to choose your resource (after adding it to Tracardi resources). When 
adding resource for Mandrill, you'll need to provide test and production API key (token).
You can get it in place where it's generated, so ```settings -> SMTP & API Info``` on
mandrillapp.com, exactly as mentioned above in Requirements. API key is 22-characters long
alphanumeric sequence, that you just need to copy from Mandrill and paste into plugin configuration.

#### Sender email
That's the email that you want to send emails from. It has to end with one of your domains
registered in Mandrill. So, for instance, if you shop is 
```exampleshop.com```, 
then you may want to send emails from address like 
```office@exampleshop.com```,
and then that's the value that you
want to insert into configuration. Please notice that this address __does not__ have to exist.

#### Message recipient's email
That's email address(es) that you want to send emails to. It can be in form
of dot path to email address (for example ```profile@pii.email```). You can also insert the address itself,
so it's independent of any data in workflow (for example you want to notify yourself every time when someone
buys something, then you just type in your own email address). Please notice that merged profiles
can have multiple values in one field - if John Doe has two or more email addresses in his profile, then
plugin will send the message to all of them.

#### Message subject
That's just message subject, if you type in ```payment```, then recipient of the message will see 
```payment``` as the subject of received message.

#### Message content
You can select if your content should be HTML or just plain text. JSON is not supported.
You can also use templates for your emails - both in HTML and text format. Examples:
##### Example 1 - plain text
```text
Hello {{profile@pii.name}}, your order will be sent in next two days.
```
Will result in changing 
```{{profile@pii.name}}``` 
to current profile's name, so John Doe will
see 
```Hello John, your order will be sent in next two days.``` 
in his message.

##### Example 2 - HTML
```html
<h1>Hello {{profile@pii.name}}!</h1>
<p>Thanks for visiting our website on {{profile@metadata.time.lastVisit}}!</p>
<p style="color:red">To thank you, we wanted to send you a photo of cute dog. Enjoy:</p>
<img src="<url-to-photo-of-cute-dog>"/>
```
Like before, recipient will see their name in the header, then our text with date of their last visit,
and then red text about photo of a dog, and a photo of this dog itself in the end.

## Tip
On Mandrill, you can turn on the test mode after clicking on you username in up-right corner.
In the test mode, you can generate test API key. You can use it in Tracardi for test purposes - 
messages won't be sent, but Mandrill will act like they are, so you can test your
configuration without being charged a single cent.




