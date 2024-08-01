# Circular Geo Fence

The Circular Geo Fence plugin for Tracardi is a location-based automation tool that enables geofencing capabilities,
allowing you to trigger actions based on geographic location.

## Version

This documentation is created for version 0.6.1 of the Circular Geo Fence plugin.

## Description

The Circular Geo Fence plugin is designed to determine whether a set of test geo-location coordinates falls within a
defined radius threshold from a center point's coordinates. This plugin can be used to create geofences for
location-based automation and personalized user experiences.

The plugin accepts a set of configuration parameters that specify the center coordinates, the test coordinates to be
evaluated, and the radius within which the test coordinates should fall to trigger an action. The output is a boolean
value, indicating whether the test coordinates are inside the defined radius.

## Inputs and Outputs

**Inputs:**

- Geofence coordinates (center and test coordinates)
- Geofence radius
- Trigger event (entry or exit)

**Outputs:**

- Returns a boolean value: __true__ if the test coordinates are inside the radius, __false__ if they are outside.

This plugin does not start the workflow; it is typically used as part of a larger automation sequence.

**Example Input (Payload):**

```json
{
  "center_coordinate": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "test_coordinate": {
    "lat": 40.748817,
    "lng": -73.985428
  },
  "radius": 10.0
}
```

**Example Output:**

```json
{
  "inside": true
}
```

## Configuration

The Circular Geo Fence plugin is configured using the following parameters:

- **Geofence Center Coordinate (Latitude and Longitude):** Specifies the central point of the geofence.

- **Geofence Test Coordinate (Latitude and Longitude):** Defines the location to be tested against the geofence.

- **Radius:** Sets the radius in kilometers within which the test coordinate should fall to trigger an action.

## JSON Configuration

```json
{
  "center_coordinate": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "test_coordinate": {
    "lat": 40.748817,
    "lng": -73.985428
  },
  "radius": 10.0
}
```

## Required Resources

This plugin does not require external resources to be configured.

## Errors

Possible errors that may occur with this plugin:

1. **Invalid Coordinate Format:** If the provided coordinates are not in the correct format (latitude and longitude),
   the plugin may raise an error.

2. **Radius Out of Range:** If the specified radius is outside a valid range (e.g., negative or excessively large), it
   may result in an error.

3. **Invalid Payload:** If the input payload is missing required fields or contains invalid data, it may cause
   unexpected errors.

4. **Configuration Issues:** Incorrect configuration parameters may lead to geofence results that do not align with
   expectations.

Please ensure that the input payload and configuration parameters are correctly formatted to avoid errors.

# Output

The plugin returns a result on the output port in the following schema:

```json
{
  "inside": true
}
```

The "inside" field indicates whether the test coordinates are inside the defined geofence (true) or outside (false).