# Last Profile Visit Time

The __Last Profile Visit Time__ plugin provides the time difference between the current time and the last visit time of
a user profile.

## Version

This documentation is for the plugin version 0.7.3.

## Description

The __Last Profile Visit Time__ plugin is used to evaluate the last visit time of a user profile. It works by assessing
the __visit__ field in the profile metadata. If a recent visit is recorded, the plugin determines the amount of time
passed since the last visit. However, if no recent visit is recorded, the plugin considers the profile insertion time as
the last visit.

It calculates the time differences in various units, such as seconds, minutes, hours, days, and weeks. If the timestamp
recorded for the last visit is not a datetime object, an error message is generated.

__Note:__ This plugin is unable to fetch visit times if no profile data is present.

# Inputs and Outputs

The plugin accepts a payload of any JSON-like object as an input.

Here's an example of a typical input:

```json
{
  "key1": "value1",
  "key2": "value2",
  ...
}
```

The output from the plugin is a JSON object containing the timestamp of the last visit (__last__) and the time
difference (__difference__) in various units.

Here's an example of a typical output:

```json
{
  "last": "2022-03-23T05:58:43.826Z",
  // timestamp of the last visit
  "difference": {
    "seconds": 60,
    "minutes": 1,
    "hours": 0.016666667,
    "days": 0.000694444,
    "weeks": 0.000099206
  }
}
```

Please note that this plugin cannot start a workflow.

# Configuration

This plugin does not require any configuration.

# JSON Configuration

This plugin does not require any configuration thus there's no JSON configuration.

# Required Resources

This plugin does not require external resources to be configured.

# Errors

The following error can occur during the operation of the Last Profile Visit Time plugin:

- "Can not get last profile visit for without a profile." - This error occurs when there is no profile data available
  for fetching the visit times.
- "Last visit is not a date. Expected datetime object got __type__." - This error occurs when the last visit time is not
  recorded as an expected datetime object. Here, __type__ is the unexpected data type of the last visit time.