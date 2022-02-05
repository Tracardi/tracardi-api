# Send to InfluxDB plugin

This plugin sends data to InfluxDB database.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns given payload on port **success** if everything went OK, or
on port **error** if an error occurred.

## Configuration

#### With form
- InfluxDB resource - Here select your InfluxDB resource, containing your token and database
  URL, that you want to send data to.
- Bucket - Here insert the name of the bucket that you want to write to. This field does not support
  the dotted notation.
- Fields - Here insert key-value pairs. Key is the name of the field of data in the bucket, and
  value is just the value for this field in added record. Feel free to use dotted notation.
- Measurement value - Here insert the path to the field containing the measurement value for the record.
- Time value - Here insert the path to the field containing time data (date, string, timestamp) for the record.
- Record tags - Here insert key-value pairs. Key is the tag key, and value is the value for this tag in this record.
- Organization - Here type in the name of your organization, that you want to upload data as. This field does not
  support the dotted notation.

#### Advanced configuration
```json
{
  "source": {
    "name": "<name-of-your-influxdb-resource>", 
    "id": "<id-of-your-influxdb-resource>"
  },
  "bucket": "<name-of-your-influxdb-bucket>",
  "fields": {
    "<field-1>": "payload@example.value",
    "<field-2>": "event@properties.example"
  },
  "measurement": "<path-to-field-containing-measurement-value>",
  "time": "<optional-path-to-field-containing-timestamp-data>",
  "tags": {
    "<tag-key-1>": "event@properties.value",
    "<tag-key-2>": "session@example.data"
  },
  "organization": "<name-of-your-influxdb-organization>"
}
```

## Warning
InfluxDB API does not always return information about error when trying to 
insert incorrect data (for example when some fields are missing). That causes plugin
to sometimes trigger **success** port, even if data has not been inserted. However,
with some major errors' occurrence (for example incorrect time field content), **error**
port is triggered properly.