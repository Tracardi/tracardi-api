# Send data to Airtable plugin

This plugin adds a new record to a given table in Airtable.

## Input
This plugin takes any payload as input.

## Output
This plugin returns record data on port **response** if everything is OK, or some
error info on port **error** if one occurs.

## Configuration
#### With form
- Airtable resource - here select your Airtable resource, containing your API key.
- Base ID - here paste in the ID of the Airtable base. You can check it while inspecting your base
  in Airtable. It looks like https://airtable.com/<BASE-ID>/...
- Table name - here simply type in the name of your table in given base.
- Record mapping - provide key-value pairs. Key is the name of the field in the table for the new record,
  and value is just a path to the value of this field, or the value itself.

#### Advanced configuration
```json
{
  "source": {
    "id": "<id-of-your-airtable-resource>",
    "name": "<name-of-your-airtable-resource>"
  },
  "base_id": "<id-of-your-airtable-base>",
  "table_name": "<name-of-your-airtable-table>",
  "mapping": {
    "field_name_1": "profile@field.example",
    "field_name_2": "event@example.field"
  }
}
```