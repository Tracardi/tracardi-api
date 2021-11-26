# Reshape payload action

This node reshapes data provided in payload, profile, 
session, or flow into another schema that is returned 
on output payload. 

# Configuration

In order to reshape the input payload user must provide 
transformation configuration. Below you can find an 
example of such configuration. Use dot notation to access json 
properties from payload, profile, etc.

You can mix regular values with values read from profile, session, etc.

```
{
  "new": {
    "key": "value",  // This is static value
    "value": "profile@id"  // Reads value from profile and saves it in object new.value
    "list": [1, "payload@data"] // Reads data value from payload and saves it as 2nf element of list
    "event": "event@..."  // Saves in event all data from event.
  }
}
```

This configuration will return an object new with the following properties.

```
{
  "new": {
    "key": "value", 
    "value": <profile_id>
    },
    "list": [
      1,
      <data_from_payload>,
    ],
    "event": <data_from_event>
}
```

## Side effects

This action does not have side effects.