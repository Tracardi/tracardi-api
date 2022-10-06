# Fetch from InfluxDB plugin

This plugin fetches data from InfluxDB resource.

## Input

This plugin takes any payload as input.

## Output

Plugin returns fetched records on port **success**, or object with some error info on **error** port if one occurs.

## Configuration

#### Form fields

- InfluxDB resource - InfluxDB resource, containing your token and database URL to the database instance.
- Organization - The name of your organization, it is the equivalent of database instance.
- Bucket - The name of the bucket that you want to write to.
- Filters - Insert key-value pairs. Key is the name of your field in InfluxDB, and value is its value. If values match,
  then the record will be returned from InfluxDB.
- Lower time bound - That's the lower time bound of your search. It can be either relative (so for example -1d), or
  fixed (2022-01-12). Path notation is fully supported.
- Upper time bound - That is the upper time bound of your search. It can be relative or fixed, path is supported as
  well.

#### JSON configuration

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
    "<field-name-2>": "1"
  },
  "start": "<lower-time-bound-for-searching>",
  "stop": "<upper-time-bound-for-searching>"
}
```