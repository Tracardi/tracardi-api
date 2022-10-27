# Decode Base64

The purpose of this plugin is to decode a base64-encoded string to its plain text form.

# Configuration

This node requires configuration.

You have to provide a path to string that needs to be transformed and set the encoding of the output string.

```json
{
  "source": "payload@path.to.data",
  "output_encoding": "utf-8"
}
```

# Input payload

This node reads a property from the input payload.

# Output

This plugin returns an object with the input property decoded from a base64 string.

# Output

*Example*

```json
{
  "text": "plain text string"
}
```