# Day/Night

This plugin, named "Day/Night," is designed to determine whether a given moment is during the day or night based on
specific geographic coordinates. It routes the workflow differently based on this determination.

# Version

0.8.2

## Description

The Day/Night plugin uses latitude and longitude data to assess whether it is currently day or night at a specific
location. It then routes the workflow through one of three possible outputs: day, night, or error. If the given
coordinates are valid and it's day time at that location, the workflow will proceed through the "day" output. If it's
night, the workflow will use the "night" output. If the plugin cannot determine the latitude and longitude, it will
route through the "error" output.

# Inputs and Outputs

Inputs:

- Payload: The plugin reads a payload object from which it extracts latitude and longitude data.

Outputs:

- Day: Returns the input payload if it is currently day time at the specified location.
- Night: Returns the input payload if it is currently night time.
- Error: Triggers if the latitude and longitude cannot be determined.

# Configuration

- __Latitude__: Set the path to latitude data or directly input the latitude value.
- __Longitude__: Set the path to longitude data or directly input the longitude value.

# JSON Configuration

Example configuration:

```json
{
  "latitude": "profile@data.devices.last.geo.latitude",
  "longitude": "profile@data.devices.last.geo.longitude"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

The Day/Night plugin works for all types of events. It does not require synchronous events.

# Errors

- "Returns error if longitude and latitude and not be found in profile": This error occurs if the plugin cannot find or
  access the latitude and longitude data in the provided payload. The workflow will proceed through the "error" output
  port in this case.
