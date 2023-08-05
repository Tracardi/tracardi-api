# Templates

Template is a text file with special mark-up. Within double curly braces you can place [dot notation](dot_notation.md) 
that reads data from [internal state of the workflow](../flow/index.md#workflow-internal-state). 

``` title="Example"
Hello {{profile@pii.name}}
```

Mark-up  `{{profile@pii.name}}` will be replaced by the data from profile.


# Read also about related topics:

* [Object template](object_template.md)
* [Dot notation](dot_notation.md)
* [Logic notation](logic_notation.md)
* [Make payload plugin](../flow/actions/reshape_payload_action.md)


---
This documentation answers the following questions:

* How to reference data in text tempaltes?
* What is the markup for data placeholders?
* How to use dot notation in text templates?
* What {{ }} does?
