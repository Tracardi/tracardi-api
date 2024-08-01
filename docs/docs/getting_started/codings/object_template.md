# Object template

There are places where you may want to create an object that consist of the data from profile, payload, memory. etc. Is
such cases you should use an object template. It will allow you to reshape the data into any object you want.

Here is an example of object template.

```
{
  "some-data": {
    "key": "value",  // This is static value
    "value": "profile@id"  // Reads value from profile and saves it in object new.value
    "list": [1, "payload@data"] // Reads data value from payload and saves it as 2nd element of list
    "event": "event@..."  // Saves in event all data from event.
  }
}
```

Notice that some parts of this object reference data with [dot notation](dot_notation.md). The data will be replaced be
the referenced data.

Let's assume that profile has the following data:

```json
{
  "id": "profile-id",
  "data": {
    "name": "John",
    "age": 26
  }
}
```

And event equals:

```json
{
  "type": "page-view",
  "properties": {
    "url": "http://localhost"
  }
}
```

then the result of the object template of:

```
{
  "some-data": {
    "key": "value",  // This is static value
    "value": "profile@id"  // Reads value from profile and saves it in object new.value
    "list": [1, "payload@data"] // Reads data value from payload and saves it as 2nf element of list
    "event": "event@..."  // Saves in event all data from event.
  }
}
```

will be:

```json
{
  "some-data": {
    "key": "value",
    "value": "profile-id",
    "list": [
      1,
      {
        "name": "John",
        "age": 26
      }
    ],
    "event": {
      "type": "page-view",
      "properties": {
        "url": "http://localhost"
      }
    }
  }
}
```
