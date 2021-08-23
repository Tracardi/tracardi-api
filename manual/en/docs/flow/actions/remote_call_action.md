# Remote call plugin

This plugin calls remote API.

# Configuration

```json
{
  "method": "get",
  "url": "http://loclhost:80/API",
  "timeout": 30,
  "headers": {
    "X-Customer-Header": "Header value"
  },
  "cookies": {
    "Cookie-Key": "Cookie value"
  },
  "sslCheck": true
}
```

This configuration defines API url as "http://loclhost:80/API".

# Payload

Payload for this plugin defines a JSON data to be sent. 

If user requires this payload to be sent with GET method than payload will be squashed to represent keys and values.

For example this JSON:

```json
{
  "payload": { 
    "mobile": "android"
  },
  "version": [10,11]
}
```

Will be flattened to parameters:

```
payload.mobile=android&version=10&verison=11
```

# Result

This plugin returns either the response (on response port) or and error on error port.

Valid response has:

```json
{
  "status": 200,
  "content": {
    ... response as json
  }
}
```
