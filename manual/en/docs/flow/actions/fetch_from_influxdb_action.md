# Fetch from InfluxDB plugin

This plugin fetches data from InfluxDB resource.

## Input
This plugin takes any payload as input.

## Output
Plugin returns fetched records on port **success**, or object with some
error info on **error** port if one occurs.

## Configuration

#### With form
- InfluxDB resource - Here select your InfluxDB resource, containing you token and your
  database URL.
- Organization - Here type in the name of your InfluxDB resource that you want to fetch data
  from. This field does not support the dotted notation.
- Bucket - Here type in the name of your InfluxDB bucket that you want to fetch data from.
  This field does not support the dotted notation as well.
- Filters - Here insert key-value pairs. Key is the name of your field in InfluxDB, and
  value is just its value. If values match, then the record will be returned from InfluxDB.
- Lower time bound - That's the lower bound of your search. It can be either relative (so for example -1d), or
  fixed (2022-01-12). Path notation is fully supported.
- Upper time bound - That is the upper bound of your search. It can be relative or fixed, path is
  supported as well.

#### Advanced configuration
```json
{
  "source": {
    "id": "<id-of-your-influxdb-resource>",
    "name": "<name-of-your-trello-resource>"
  },
  "organization": "<name-of-your-influxdb-organization>",
  "bucket": "<name-of-your-influxdb-bucket>",
  "filters": {
    "<field-name-1>": "payload@example.value",
    "<field-name-2>": "profile@value.example"
  },
  "start": "<lower-time-bound-for-searching>",
  "stop": "<upper-time-bound-for-searching>"
}
```