# String splitter

This plugin strips the given string off all the characters that appear in to_remove string.

# Configuration

Example:

```json
{
  "string": "Hello, World!",
  "to_remove": "Ho"
}
```

This configuration will strip off the string `Hello, World!` off of the character `Ho`,
resulting in `ell, Wrld!`.

# Output

Returns the string with the specified characters removed.

Example:

```json
{
  "value": "ell, Wrld!"
}
```
