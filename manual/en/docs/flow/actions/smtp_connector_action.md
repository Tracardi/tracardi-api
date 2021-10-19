# SMTP Plugin

The purpose of this plugin is to send e-mail using SMTP servers. The plugin supports sending HTML messages.

# Configuration

This node requires configuration.

## Message configuration

* to: None, - Choose `e-mail` recipient
* from: None, - Choose your `e-mail`
* replyTo: None,- Select to whom the reply should be sent
* title: Select a `title`,
* message: Enter your `message`, HTML is allowed

## Resource configuration

This node needs SMTP server credentials that are defined in resources. To access defined credentials you will have to
pass resource id.

## Example of action configuration

```json
{
  "message": {
    "send_to": "to@email.com",
    "send_from": "from@email.com",
    "reply_to": "reply-to@email.com",
    "title": "E-mail title",
    "message": "E-mail message"
  },
  "source": {
    "id": "resource-id"
  }
}
```

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
