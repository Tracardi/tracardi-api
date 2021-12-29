# Event validation

Events can be validated. Event validation can be configured in the Tracardi GUI or via the API. The endpoints
responsible for creating the validation schemes are located at the following endpoints:

| Method      | Path                                  |                          |
| ----------- | --------------------------------------|--------------------------|
| `GET`       | /event/validation-schema              | Add validation schema    |
| `DELETE`    | /event/validation-schema/{event_type} | Delete validation schema |
| `GET`       | /event/validation-schemas             | List validation schemas  |

As always, complete API documentation is available at:

```
http://tracardi-host:8686/docs
```

## New event validation schema

To add new event validation schema that you will need to provide a Json Schema object that defines the model of event,
or event session or loaded profile.

Validator consist of 2 elements. Data to be validated - expressed in a [dotted notation](../notations/dot_notation.md), and a
json schema itself.

```json
{
  "event@properties": {
    ...json-schema
  },
  "profile@traits.public.my-data": {
    ...json-schema
  }
}
```

*Real example* - for event@properties

```json
{
  "validation": {
    "event@properties": {
      "type": "object",
      "properties": {
        "price": {
          "type": "number"
        },
        "name": {
          "type": "string"
        }
      },
      "required": [
        "name"
      ]
    }
  },
  "event_type": "test"
}
```

## Validation caching

Validation is cached and the default Time To Live for cache is 180 seconds. It means that validation schema will stay
the same for 3 minutes even if it was change by the user. It will be red again after 180 seconds. To make the period
longer or shorter, run Tracardi with environment variable EVENT_VALIDATOR_TTL set to the number of seconds you would
like the system to cache the validation.

## Validation errors

If the validations does not pass an error 406 - NOT ACCEPTABLE status is returned with the information on the reason why
the validation did not pass.

```json
{
  "detail": "Validation failed with error: event@properties: 'name' is a required property...."
}
```