# Validate with JSON schema plugin

This plugin validates objects using provided JSON schema.

## Input
This plugin takes any payload as input.

## Outputs
This plugin returns payload on port **OK** if validation is passed, or payload
on port **ERROR** if validation fails.

## Configuration

#### With form
- JSON validation schema - Here provide validation schema in form of JSON.

#### Advanced configuration
```json
{
  "validation_schema": "<validation-object>"
}
```

Example of valid schema to provide in the form field or as a value of **validation_schema**:
```json
{
 "payload@properties.sale":{
    "type" : "object",
     "properties" : {
         "price" : {"type" : "number"},
         "name" : {
           "type" : "string", 
           "maxLength": 15
         }
     }
 },
 "profile@context.timestamp": {
     "type": "integer"
  }
}
```