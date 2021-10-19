# GeoLite2 plugin

This plugin connects geoIP servers and returns location of the customer based on the provided ip address.

# JSON Configuration

Example:

```json
{
  "source": {
    "id": "5600c92a-835d-4fbe-a11d-7076fd983434"
  },
  "ip": "payload@ip"
}
```

IP value can be a path to value in profile, payload, or event or IP address itself.

## Resource configuration

To run this plugin you must provide source id that has configured GeoLite2 server credentials.

Example of source configuration for GeoLite2 API:

```json
{
  "host": "geolite.info",
  "license": "<license-key>",
  "accountId": "<account-id>"
}
```

You must provide `license-key` and `account-id` to connect to MaxMind GeoLite2 API.
