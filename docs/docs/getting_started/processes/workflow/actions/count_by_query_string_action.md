# Count records by query string plugin

This plugin counts records is given index, that match given query and are within
given time range.

## Input
This plugin takes any payload as input.

## Output
This plugin returns number of records on port **result**, or optional error
information on port **error** if one occurs.

## Plugin configuration

#### With form
- Index - please select index that you want to count records in.
- Time range - please provide some time offset expression like **-14d** or **-15 minutes**.
  Negative values are not allowed.
- Query string - here provide regular Elasticsearch query string. It can be provided in form
  of dot template, so for example **profile.id:{{profile@id}} AND type:page-view**

#### Advanced configuration
```json
{
  "index": "event | session | profile",
  "time_range": "<valid-negative-time-expression>",
  "query": "<valid-elasticsearch-query-string>"
}
```
