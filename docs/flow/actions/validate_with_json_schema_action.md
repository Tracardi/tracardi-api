# Validate with JSON schema plugin

This plugin validates objects using provided JSON schema.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns payload on port **TRUE** if validation is passed, or payload on port **FALSE** if validation fails.
If the schema is incorrect then the **ERROR** port is triggered. 

#### JSON configuration

```json
{
  "validation_schema": "<validation-object>"
}
```

Example of valid schema to provide in the form field or as a value of **validation_schema**:

```json
{
  "payload@properties.sale": {
    "type": "object",
    "properties": {
      "price": {
        "type": "number"
      },
      "name": {
        "type": "string",
        "maxLength": 15
      }
    }
  },
  "profile@context.timestamp": {
    "type": "integer"
  }
}
```

```json
 {
    "payload@...": {
      "title": "Product",
      "description": "A product from Acme's catalog",
      "type": "object",
      "properties": {
        "productId": {
          "description": "The unique identifier for a product",
          "type": "integer"
        }
      },
      "required": [
        "productId"
      ]
    }
  }
```