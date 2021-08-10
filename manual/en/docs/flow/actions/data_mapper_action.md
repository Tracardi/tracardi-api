# Data mapper

This node reshapes data provided in payload, profile, 
session, or flow into another schema that is returned 
on output payload. 

# Configuration

In order to reshape the input payload user must provide 
transformation configuration. Below you can find an 
example of such configuration. Use dot nottaion to access json 
properties from payload, profile, etc.

```json
{
  "new.value.from.profile": "profile@id",  // Reads value from profile and saves it in object new.value.from.profile
  "new.list.0": "payload@data", // Reads data value from payload and saves it as 1st element of list new.value.from.profile
  "new.list.1": "b", // Saves as 2nd value of new.list
  "new.objectList.0.a": 1, // Saves object property a as 1st element of list new.objectList
  "new.objectList.0.b": 2
}
```

This configuration will return an object new with the following properties.

```json
{
  "new": {
    "value": {
      "from": {
        "profile": <profile_id>
      }
    },
    "list": [
      <data_from_payload>,
      "b"
    ],
    "objectList": [
      {
        "a": 1,
        "b": 2
      }
    ]
  }
}
```

## Side effects

This action does not have side effects.