# Send to InfluxDB plugin

This plugin sends data to InfluxDB database.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns given payload on port **success** if everything went OK, or on port **error** if an error occurred.

# InfluxDB data structure

Data in influxDb is more complex than regular data. It has on top Organisation, this is the equivalent of database
instance. Bucket is the equivalent of database in SQL. Measure is a table, fields and values are records (e.i: columns
and values in one record). Tags are additional metadata. Time is a timestamp of a particular set of fields (record).

## Configuration

#### Form description

- InfluxDB resource - InfluxDB resource, containing your token and database URL to the database instance.
- Organization - The name of your organization, it is the equivalent of database instance.
- Bucket - The name of the bucket that you want to write to.
- Fields - Record in a key-value pairs format. Key is the name of the field of data in the bucket, and value is the
  value for this field in a record. Feel free to use dotted notation for value part.
- Measurement name - Measurement name for the record.
- Time - Path to the field containing date of the record. This parameter is optional. Invalid data of date format will
  be ignored and date time will be set to the moment of the execution.
- Record tags - Key-value pairs. Key is the tag name, and value is the value for this tag.

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
  "measurement": "<measurement-name>",
  "time": "<optional-path-to-field-containing-timestamp-data>",
  "tags": {
    "<tag-key-1>": "event@properties.value",
    "<tag-key-2>": "session@example.data"
  },
  "organization": "<name-of-your-influxdb-organization>"
}
```

## Warning

InfluxDB API does not always return information about error when trying to insert incorrect data (for example when some
fields are missing). That causes plugin to sometimes trigger **success** port, even if data has not been inserted.
However, with some major errors' occurrence (for example incorrect time field content), **error**
port is triggered properly.