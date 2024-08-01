# String to Date

The String to Date plugin is used to convert a string representing a date into a date object. This can be useful for
transforming date strings from various sources into a consistent format for further processing in your workflows.

## Version

This documentation is for plugin version 0.8.2.

## Description

The String to Date plugin takes a date string as input and attempts to convert it into a date object. If the conversion
is successful, it returns the date object on the "date" output port. If the conversion fails, it returns an error
message on the "error" output port.

The plugin uses the [dateparser](https://dateparser.readthedocs.io/en/latest/) library to parse date strings. The date
string to be converted is specified in the plugin's configuration.

**Example:**

If the plugin is configured with a date string like "2023-10-12," it will attempt to convert this string into a date
object representing October 12, 2023.

## Inputs and Outputs

- **Input**: This plugin has one input port named "payload," which accepts any payload data.

- **Outputs**:
    - "date": If the date string is successfully converted, the date object is returned on this port.
    - "error": If the conversion fails, an error message is returned on this port.

## Configuration

The String to Date plugin has the following configuration parameters:

- **String**: This is where you specify the path to the text or the text itself that you want to convert to a date. The
  plugin will attempt to convert the value located at this path within the payload.

## JSON Configuration

Here is an example of the JSON configuration for the String to Date plugin:

```json
{
  "string": "event@path.to.date.string"
}
```

In this example, the plugin is configured to convert the date string located in event at "path.to.date.string".

## Required Resources

This plugin does not require external resources to be configured.

## Errors

The String to Date plugin may encounter the following error:

- **Error Message**: If the date string provided in the configuration cannot be parsed as a date, an error will be
  generated.

- **When It May Occur**: This error may occur if the date string is not in a valid format or if the parsing process
  encounters an issue. It's essential to ensure that the date strings provided are in a format that can be recognized by
  the dateparser library.

---

*Note: This plugin's functionality relies on the dateparser library, so the success of date conversion depends on the
library's ability to parse the provided date string.*