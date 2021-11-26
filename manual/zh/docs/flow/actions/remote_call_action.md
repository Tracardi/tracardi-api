# Remote call plugin

This plugin calls remote API.

# Configuration

```json
{
  "method": "post",
  "url": "http://localhost:80/API",
  "timeout": 30,
  "headers": {
    "X-Customer-Header": "Header value"
  },
  "cookies": {
    "Cookie-Key": "Cookie value"
  },
  "sslCheck": true,
  "body": {
    "content": "{\"json\":1}",
    "type": "application/json"
  }
}
```

This configuration defines API url as POST "http://loclhost:80/API" with body `{"json":1}`.


If user requires the body to be sent with GET method than body will be squashed to represent keys and values.

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

*Example of valid response*

```json
{
  "status": 200,
  "content": "<body>",
  "cookies": {
    "key": "value"
  }
}
```
