# E-mail via SMTP

The purpose of this plugin is to send e-mail using SMTP servers. The plugin supports sending HTML messages.

# Configuration

This node requires configuration.

## Example of configuration

```json
{
  "message": {
    "send_to": "to@email.com",
    "send_from": "from@email.com",
    "reply_to": "reply-to@email.com",
    "title": "E-mail subject",
    "message": "My name is {profile@traits.private.pii.name}"
  },
  "source": {
    "id": "resource-id"
  }
}
```

## Configuration description

* to: None, - Choose `e-mail` recipient
* from: None, - Choose your `e-mail`
* replyTo: None,- Select to whom the reply should be sent
* title: Enter a `E-mail subject`,
* message: Enter your `message`, HTML is allowed as well as message template.

### Message

Message can be a Tracardi template. Tracardi templates can merge plain text or HTML with data from profile, event, 
or session. 

*Example of Tracardi message template*

```
My name is {profile@traits.private.pii.name}
```

The `{profile@traits.private.pii.name}` placeholder will be replaced by data from profile. Path to data is 
`traits.private.pii.name`.


## Resource configuration

This node needs SMTP server credentials that are defined in resources. To access defined credentials you will have to
pass resource id.

# Resources

This node needs access to resource that configures SMTP server credentials:

Needed credentials:

* smtp: smtp.gmail.com, - Choose a smtp server
* port: 587, - Select the port on which smtp will run
* username: None, - enter your username
* password: None, - enter your password
* timeout: 15

## Example of resource configuration

```json
{
  "smtp": "smtp.gmail.com", 
  "port": 587, 
  "username": "enter your username",
  "password": "enter your password",
  "timeout": 15
}
```

# Input payload

This node does not process input payload.

# Output

This node returns `true` if mail was sent or `false` if there was an error.
