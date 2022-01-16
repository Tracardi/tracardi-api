# Regex string replace plugin

This plugin takes string as an input and replaces its fragments that match
given regex.

## Input
This plugin takes any payload as input.

## Output
This plugin returns regex after operations on port **replaced** if matches were found,
or given string on port **not_found** if given value was not containing any fragment
matching given regex.

## Configuration

#### With form
- String - Type a path to the string that you want to substitute.
- Replace with - Type a path to a string to substitue with.
- Regex - Here provide the regex that will match the fragments that you want to replace.

#### Advanced configuration
```json
{
  "string": "<path-to-string-that-you-want-to-operate-on>",
  "find_regex": "<regex-that-will-match-fragments-to-replace>",
  "replace_with": "<path-to-string-that-you-want-to-replace-with>"
}
```