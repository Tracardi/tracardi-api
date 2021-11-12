# Template Plugin

Plugin is configured with template:

*Example*
```
Hello {{profile@pii.name}}
```

where `profile@pii.name` is path to variable in payload in dot notation. 

Plugin returns string with placeholder replaced with values form workflow internal state.