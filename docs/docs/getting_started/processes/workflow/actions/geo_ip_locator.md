# GeoLite2 Plugin

The "GeoLite2" plugin in Tracardi connects to GeoIP servers and provides location information based on the provided IP
address. This plugin is useful for retrieving geographical data about customers or users.

## JSON Configuration

The configuration for the "GeoLite2" plugin is specified in JSON format. Here is an example configuration:

```json
{
  "source": {
    "id": "5600c92a-835d-4fbe-a11d-7076fd983434"
  },
  "ip": "payload@ip"
}
```

In the configuration, you need to provide the ID of the source that has the configured GeoLite2 server credentials.
The `ip` field specifies the path to the IP value in the profile, payload, or event, or it can be an IP address itself.

## Resource Configuration

To run the "GeoLite2" plugin, you must provide a source configuration that contains the credentials for the GeoLite2
API. The source configuration for the GeoLite2 API should include the following information:

```json
{
  "host": "geolite.info",
  "license": "<license-key>",
  "accountId": "<account-id>"
}
```

You need to replace `<license-key>` and `<account-id>` with the actual values provided by MaxMind for your GeoLite2 API
access.

## Output

The output of the "GeoLite2" plugin is a JSON object that provides the following location information:

```json
{
  "city": "<city>",
  "country": {
    "name": "<country>",
    "code": "<country-code>"
  },
  "county": "<county>",
  "postal": "<code>",
  "latitude": 52.0979,
  "longitude": 18.2016
}
```

The `city` field represents the city name, the `country` field provides the country name and country code, the `county`
field specifies the county name, the `postal` field contains the postal code, and the `latitude` and `longitude` fields
represent the geographical coordinates of the location.

Please refer to the Tracardi documentation for more information on how to configure and use the "GeoLite2" plugin.

## Plugin Configuration

The "GeoIP Action" plugin has the following configuration options:

- **Maxmind Geolite2 connection resource**: This option allows you to select a Maxmind Geolite2 server resource. The
  credentials from the selected resource will be used to connect to the GeoIP service.

- **Path to IP**: In this field, you can specify the path to the IP data in the payload or directly provide the IP
  address itself. The plugin will use this IP address to fetch the location information.

## Plugin Outputs

The "GeoIP Action" plugin has two output ports:

- **location**: This port returns the location information as a result of converting the IP address. The location
  information includes the city, country name, country code, county, postal code, latitude, and longitude.

- **error**: If an error occurs during the execution of the plugin, this port will be triggered. The payload and the
  error message will be provided in the output.

## Example Usage

Here's an example of how the "GeoIP Action" plugin can be used:

```yaml
- geoip_action:
    source:
      id: "5600c92a-835d-4fbe-a11d-7076fd983434"
    ip: "event@request.ip"
```

In this example, the plugin is configured to use a Maxmind Geolite2 server resource with the specified ID. It retrieves
the IP address from the "event@request.ip" field and converts it to location information. The location data is returned
on the "location" port.

