# Regex string replace plugin

This plugin takes string as an input and replaces its fragments that match
given regex.

## Input
This plugin takes any payload as input.

## Output
This plugin returns regex after operations on port **replaced** if matches were found,
or given string on port **not_found** if given value was not containing any fragment
matching given regex.

## JSON Configuration

```json
{
  "string": "<path-to-string-that-you-want-to-operate-on>",
  "find_regex": "<regex-that-will-match-fragments-to-replace>",
  "replace_with": "<path-to-string-that-you-want-to-replace-with>"
}
```