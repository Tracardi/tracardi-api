# Remote call plugin

This plugin calls remote API.

# Configuration

```json
{
  "method": "post",
  "source": {
    "id": "<id-of-API-resource>",
    "name": "<name-of-API-resource>"
  },
  "endpoint": "/some/endpoint/{event@with.template}/here",
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

This configuration makes POST request to API URL from selected resource with body `{"json":1}`.

If user requires the body to be sent with GET method than body will be squashed to represent keys and values.

For example this JSON:

```json
{
  "payload": {
    "mobile": "android"
  },
  "version": [
    10,
    11
  ]
}
```

Will be flattened to parameters:

```
payload.mobile=android&version=10&version=11
```

This plugin supports dot paths in cookie headers and body - you can use them like this:

```json
{
  "headers": {
    "X-Custom-Header": "payload@some.field"
  }
}
```

Paths will be replaced with current workflow values.

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
