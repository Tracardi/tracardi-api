# Discord webhook plugin

This plugin sends discord messages.

# Configuration

Configuration needs a discord webhook url. Webhooks can be created in discord application. Click settings in the channel 
that you would like to send message to.  Then click integrations and webhooks.  Expand webhook list and click 
new webhook. Give it a name and copy url. This url should be copied to URL in the configuration JSON.

```json
{
  "url": "https://discord.com/api/webhooks/879132030/kXYSPpId...",
  "timeout": 10,
  "message": "Hello {{profile@traits.private.name}}",
  "username": "<username>"
}
```

# Input

This plugin does not process input payload. 

# Output

This plugin returns either the input payload on response port or and error on error port.

