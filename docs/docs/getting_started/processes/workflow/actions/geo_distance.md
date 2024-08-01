# Geo distance

This plugin is used to calculate the geographical distance between two points: the start point and the end point. Those points are represented by their geographical coordinates (latitude and longitude). 

# Version

The documentation is valid for the plugin version 0.6.1. 

## Description

The Geo distance plugin is designed to calculate the distance between two geographical points which are specified using their latitude and longitude coordinates. The starting coordinates are predefined in the plugin’s configuration, while the ending coordinates can be specified in each run of the plugin, which allows for processing different locations within a single configuration of the plugin.
 
The result of the plugin's execution is a measurement of the distance in kilometers between the starts and end points. This distance is returned via the "payload" port. 

# Inputs and Outputs

The Geo distance plugin has one input port and one output port:
- The input port is named "payload". It accepts a dictionary with keys that correspond to the latitude and longitude of the end point.
- The output port is named "payload". It returns a dictionary containing a single key "distance" with the calculated distance in kilometers as its value.

The plugin cannot start the workflow, so it needs some data provided by the previous action in the workflow via the "payload" port.

# Configuration

The configuration of Geo distance comprises two parts, which are the geographical coordinates for the start point:

- The start_coordinate.lat: the latitude of the start point.
- The start_coordinate.lng: the longitude of the start point.

# JSON Configuration

```json
{
    "start_coordinate": {
        "lat": "52.228847",
        "lng": "21.003748"
    }
}
```
In the above JSON configuration example, the start point is set to the coordinates of Warsaw, Poland.

# Required resources

This plugin does not require external resources to be configured.

# Errors

Currently, this plugin does not generate errors. However, given the nature of geographical coordinates, it's essential to ensure the input values fall within the valid range. That is, latitude should be a value between -90 and 90 and longitude should be a value between -180 and 180. If the plugin receives invalid coordinates, the calculated distance may be incorrect.