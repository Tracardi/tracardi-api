# String Replace

This plugin is designed to replace a specific substring within a text field in the payload of a Tracardi workflow. It's
particularly useful for modifying text data, such as correcting misspellings or standardizing terminology.

# Version

0.8.2

## Description

The String Replace plugin operates on a specified field in the workflow's payload. It searches for a defined substring (
the 'find' value) and replaces it with another string (the 'replace' value). For instance, if the field contains "Hello
World" and the find value is "World", replacing it with "Tracardi" would change the text to "Hello Tracardi". The plugin
then updates the payload with this new value. If the specified field is not a string, the plugin returns an error
message.

# Inputs and Outputs

- **Inputs**: The plugin accepts a payload object which should contain the field to be operated on.
- **Outputs**:
    - **Output**: Returns the modified value with the string replacement applied.
    - **Error**: If the specified field is not a string, an error message is returned.

# Configuration

- **Field**: The field for string replacement.
- **Find**: The substring to be replaced.
- **Replace**: The string to replace the found substring.

# Result

Example:

```json
{
  "value": "string with replaced substring"
}
```

# JSON Configuration

Example configuration:

```json
{
  "field": "profile@data.exampleField",
  "find": "oldText",
  "replace": "newText"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- **"Field '{field}' is not a string."**: This error occurs if the specified field in the payload is not a string type.
  For example, if a numeric or object field is specified, this error will be returned.
