# Encode Base64

The purpose of this plugin is to encode a plain text string as base64.

# Configuration

This node requires configuration.

You have to provide a path to string that needs to be transformed and set the encoding of the input string.

```json
{
  "source": "payload@path.to.data",
  "source_encoding": "utf-8"
}
```

# Input payload

This node reads a property from the input payload.

# Output

This plugin returns an object with the input property encoded as base64 string.

# Output

*Example*

```json
{
  "base64": "aGVsbG8gdHJhY2FyZGkh"
}
```