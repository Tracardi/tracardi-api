# Time Difference

This plugin, Time Difference, calculates the difference between two dates.

# Version

0.6.0.1

## Description

The Time Difference plugin calculates the time difference between two given dates. These dates are provided using the
dot notation from the payload. The dates can be of any format, but they're often either a string which represents a date
or a Python datetime object.

The Time Difference plugin takes two inputs - a reference date (the starting point) and a secondary date (the end
point). It uses these inputs to compute the time difference in various units: seconds, minutes, hours, days, and weeks.

Steps:

1. The plugin first retrieves the payload passed to it. It uses a DotAccessor to extract the dates defined in the
   configuration from this payload.
2. For each date, it performs a check. If the input is a string and equals 'now', the plugin substitutes it with the
   current date and time (in UTC). If it's simply a string that represents a date, it parses the string into a datetime
   object. If it's already a datetime object, it uses the datetime as it is. If none of these conditions are met, it
   raises an exception.
3. Once both dates are ensured to be datetime objects, the plugin calculates the difference between these two dates. It
   does this by subtracting the reference date from the secondary date.
4. The resulting time delta (difference), originally in seconds, is converted into minutes, hours, days, and weeks for
   convenience.

Note: If the reference date is later than the secondary date ('now' or otherwise), the values returned by the plugin
will be negative.

# Inputs and Outputs

The Time Difference plugin accepts two inputs using the payload:

1. __reference_date__ : It is the starting point for time difference calculation. It can be in any format - a string
   representing a date/time, or a Python datetime object,
2. __now__ : It is the end point for time difference calculation. It can also be in any format - a string representing a
   date/time, the string 'now' to use the current date/time, or a Python datetime object.

Once the plugin finishes execution, it returns the time difference on the port "time_difference". The result is a
dictionary containing the time difference in various units : seconds, minutes, hours, days, and weeks.

## Configuration

The Time Difference plugin needs to be configured with dot notation paths to two dates -

- __Reference date__ : The path in the payload to the reference date, i.e., the start date.
- __Second date__ : The path in the payload to the second date, i.e., the end date. The configuration accepts the
  string 'now' in place of a path to signify the current UTC time.

# JSON Configuration

Here's an example configuration in JSON format:

```JSON
{
  "reference_date": "event@session.start",
  "now": "event@session.end"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- "Could not parse data __{}__": This error is raised when the plugin fails to parse the provided date. It usually occurs
  when the provided date does not follow a recognizable format.
- "Date can be either string or datetime object": This error is raised when the plugin encounters a date input that
  isn't a string or datetime object. It may occur if the data at the payload path provided in the configuration is
  neither a string nor a datetime object.