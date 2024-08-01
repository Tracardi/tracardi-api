# Templates

Template is a text file with special mark-up. Within double curly braces you can place [dot notation](dot_notation.md) 
that reads data from internal state of the workflow. 

``` title="Example"
Hello {{profile@pii.name}}
```

Mark-up  `{{profile@pii.name}}` will be replaced by the data from profile.
