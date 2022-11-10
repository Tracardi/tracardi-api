# Google event tracker

This plugin sends event to google analytics

# JSON Configuration

```json
{
  "category": "category",
  "action": "action",
  "label": "label",
  "value": 0
}
```

* __Category__ (required): The category of the event you’re tracking. The category organizes events into groups. Example:
  Buttons.
* __Action__ (required): The action of the event you’re tracking. The action tells you what a visitor did. Example: Click.
* __Name__ (optional): The name of the event you’re tracking. The name gives you more information about the event. Example:
  Sign up (a CTA on your button).
* __Value__ (optional): The value you want to assign to the event you’re tracking. Example: 5. If an action is worth some
  money for your business, like a signup button click is worth 5 USD, you can assign a value for it. Every time an event
  happens.

# Output 

Returns result on the output port in the following schema:

```json
{
  "status": "200",
  "content": "response content"
}
```