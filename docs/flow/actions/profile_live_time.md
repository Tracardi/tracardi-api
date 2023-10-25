# Profile live time

This plugin returns the duration for which a profile has existed in the system.

# Version

0.8.0

## Description

The plugin works by finding the date and time when the profile was created. It then calculates the difference between
the current time and the creation time in various units such as seconds, minutes, hours, days, and weeks, and returns
this information. However, if the profile is not present or the creation time is not a Date-Time object, it returns an
error along with the payload.

# Inputs and Outputs

- Inputs:
    + The plugin takes any JSON-like object as an input through the payload input port.
- Outputs:
    + If the process is successful, the plugin returns the duration for which the profile has existed in the various
      time units mentioned above. This duration is returned through the "live-time" output port.
    + If there is an error (for example, if the profile is not present or the creation time is not a Date-Time object),
      the plugin returns the error message along with the payload through the "error" output port.

# Configuration

The plugin does not have any configuration parameters.

# JSON Configuration

Since the plugin does not have any configuration parameters, it does not require a JSON configuration.

# Required resources

This plugin does not require any external resources to be configured.

# Errors

- "Can not get profile live time without a profile.": This error occurs when there is no profile present.
- "Profile time.insert is not a date. Expected datetime object got {type(created)}.": This error occurs when the
  creation time of the profile is not a Date-Time object. The placeholder {type(created)} is replaced with the actual
  type of the creation time.