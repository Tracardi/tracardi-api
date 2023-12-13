# GeoIp service

This plugin, named 'GeoIp service', is designed to convert an IP address into detailed location information. It
leverages MaxMind's GeoLite2 services to identify the geographical location associated with a given IP address.

# Version

0.6.1

## Description

When the GeoIp service plugin receives an IP address, it communicates with the MaxMind GeoLite2 server to fetch location
data corresponding to that IP. This data includes city, country (with name and ISO code), county, postal code, and
geographic coordinates (latitude and longitude). If configured, the plugin can also add the fetched location details to
the user's profile, updating the last known location of the device. The plugin outputs the location data, and in case of
any errors during the process, it provides an error output with details.

# Inputs and Outputs

- __Inputs__: The plugin takes a payload object, which should contain the IP address.
- __Outputs__: There are two output ports:
    - __location__: Outputs location details in a structured format.
    - __error__: Triggered if there is an error during execution, providing details of the payload and error.

# Configuration

- __Source__: Select the Maxmind Geolite2 server resource for connecting to the service.
- __IP Path__: Specify the path to the IP data or directly input the IP address.
- __Add to Profile__: Choose whether to add the discovered location to the profile's last device location.

# JSON Configuration

Example configuration:

```json
{
  "source": {
    "id": "5600c92a-835d-4fbe-a11d-7076fd983434",
    "name": "MaxMind Geo Locator"
  },
  "ip": "payload@ip",
  "add_to_profile": false
}
```

# Required resources

This plugin requires the configuration of an external resource: a Maxmind Geolite2 server. The resource should include
credentials such as the host, license key, and account ID.

# Errors

- "An error occurred during location fetching": This message indicates a failure in retrieving location information from
  the GeoLite2 server. It may occur due to network issues, incorrect resource configuration, or invalid IP address
  input.
- "Failed to update the profile with location data": This error occurs if there is an issue in adding the fetched
  location to the user's profile, possibly due to profile access or update rights.
