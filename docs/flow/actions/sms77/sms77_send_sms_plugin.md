# Send SMS with Sms77 gateway

This plugin sends SMS with sms77 gateway. 

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns response from Sms77 API on port **response**, or optional error info on port **error** if one
occurs.


## JSON Configuration

Json configuration contains of resource, message, recipient, and sender.

```json
{
  "resource": {
    "id": "",
    "name": ""
  },
  "message": "",
  "recipient": "profile@pii.telephone",
  "sender": ""
}
```

### Message

Massage is a message template. That means you can use template placeholders.  

#### Example 

```text
Hello {{profile@pii.name}}, your order will be dispatched in next two hours.
```

This message will have the **{{profile@pii.name}}** changed to the current profile's name, so the recipient will
see **'Hello John, your order will be dispatched in next two hours.'** in his SMS.

### Sender

Please leave sender blank if you want to use default sms77 sender. If you would like to use custom sender phone number 
please set the sender in sms77 system and paste its number or name here. 

### Recipient

Recipient can be pointed from the profile (default value comes from profile@pii.telephone) or it can be static phone
number e.g. "+49374882833"

