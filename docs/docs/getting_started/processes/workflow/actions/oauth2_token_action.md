# Get OAuth2 token plugin

## Inputs
This plugin takes any payload object.

## Outputs
This plugin outputs given payload object modified according to configuration.

## Config

#### With form
- API endpoint resource - here select your API-endpoint-type resource that you
want to get a token from.
- Token destination - here type in path to a field (starting with **'payload@'**),
where you want to store an object returned by endpoint.

#### Advanced config
```json
{
  "source": {
    "id": "<id-of-your-api-endpoint-resource>",
    "name": "<name-of-your-api-endpoint-resource>"
  },
  "destination": "<dot-path-to-destination-field>"
}
```
Where destination field is the field where you want to store received object. This path
has to start with **'payload@'**.