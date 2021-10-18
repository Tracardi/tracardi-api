# Zapier plugin

This plugin calls zapier webhook API.

# Configuration

```json
{
  "url": "https://hooks.zapier.com/hooks/catch/10523213728/b4basesz/"
}
```

This configuration requires zapier webhook url.

# Payload

Payload for this plugin defines a JSON data to be sent. It can be any json schema.

# Result

This plugin returns either the response (on response port) or and error on error port.

Valid response is:

```json
{
  "status": 200,
  "content": {
    ... response as json
  }
}
```