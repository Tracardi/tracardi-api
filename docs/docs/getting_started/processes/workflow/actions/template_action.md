# Template Plugin

Returns a string build from template.

# Input

Plugin requires template that contains placeholders with referenced data. Placeholders start with {{ and end with }}.
Placeholders are replaced by the referenced data. See how to [reference data](../../../codings/dot_notation.md) for more information: 

*Example*
``` 
Hello {{profile@pii.name}}
```

where `profile@pii.name` is path to variable in payload that is located at __pii.name__. 

Plugin returns string with placeholder replaced by values from referenced data. See [workflow internal state](index.md) 
for more information on data saved inside workflow.

# Output

*Example*

```json
{
  "template": "Hello Adam"
}
```