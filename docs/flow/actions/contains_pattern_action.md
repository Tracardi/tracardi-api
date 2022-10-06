# Contains Pattern Plugin

This plugin __checks if data field contains selected pattern__. It is capable to match single patterns for the whole string
or search for all the patterns in given string. Chose ALL to look for patterns in the text regardless if the patterns
is inside the text or the whole text contains pattern.

When you select the single pattern this plugin will search for the pattern and will return its value only if the whole
text contains pattern. E.g. This string: "My email is email@email.com" __will not be matched__ if single e-mail pattern is
selected as the string contains other information besides e-mail. If you want to search for email in this pattern 
select ALL.

## JSON Configuration

Example config:

```json
{
  "field": "payload@field",
  "pattern": "all"
}
```

### Available patterns
* *url* - checks if data field contains exactly URL e.g. https://www.google.com 
* *ip* - checks if data field contains exactly ip address
* *date* - checks if data field contains exactly date in dd-mm-yyyy format
* *email* - checks if data field contains exactly email address
* *all* - checks if data field contains all the patterns listed above

Output:

Plugin returns found patterns on port TRUE or FALSE if no patterns were found.

### Output examples

Output for single pattern match

```json
{
  "email": ["test@test.com"]
}
```

Output for multiple pattern match

```json
{
  "date": ["2022-01-01"],
  "email": ["test@test.com", "admin@admin.com"]
}
```