# Fetch data from Airtable plugin

This plugin fetches data from given Airtable table, according to provided query.

## Input

This plugin takes any payload as input.

## Output

This plugin returns records on port **response** if everything is OK, or some error info on port **error** if one
occurs.

## Configuration

#### Form fields

- Airtable resource - here select your Airtable resource, containing your API key.
- Base ID - here paste in the ID of the Airtable base. You can check it while inspecting your base in Airtable. It looks
  like https://airtable.com/<BASE-ID>/...
- Table name - here simply type in the name of your table in given base.
- Formula - you can add some query. It's optional and supports dot templates, example:
  **{profileID} = {{profile@id}}** will match every record, where value of **profileID** field is equal to current **
  profile@id** value.

#### JSON configuration

```json
{
  "source": {
    "id": "<id-of-your-airtable-resource>",
    "name": "<name-of-your-airtable-resource>"
  },
  "base_id": "<id-of-your-airtable-base>",
  "table_name": "<name-of-your-airtable-table>",
  "formula": "<optional-query-formula>"
}
```