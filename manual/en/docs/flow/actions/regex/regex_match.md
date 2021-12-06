# Regex Match

The purpose of this plugin is to display particular groups of regexes that we specify in a pattern.

# Configuration

This node requires configuration.

## Example of configuration

```json
{
  "pattern": "(\\b[A-Z]+\\b).+(\\b\\d+)",
  "text": "The price of PINEAPPLE ice cream is 20",
  "group_prefix": "Group"
}
```

## Output example:

```json
{
  "Group-A": "PINEAPPLE",
  "Group-B": "20"
}
```

## Configuration description

* *pattern* - Provide regex pattern.
* *text* - Enter your text. You can use dot notation to access profile or event data.
* *group_prefix* - Enter the prefix for groups

## Examples of errors

- Regex couldn't find anything matching the pattern from supplied string. - This means that the pattern you specified is
  incorrect, because the plugin cannot find any text. This error will not stop workflow but will be logged as a warning.

# Input payload

This node does not process input payload.

# Output

This node returns dictionary containing matched data with groups

*Example*

```json
{
  "Group-A": "PINEAPPLE",
  "Group-B": "20"
}
```