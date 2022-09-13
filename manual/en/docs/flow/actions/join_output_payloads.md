Joins payload from incoming data.

# Data join

This plugin will join data form input connections. If the connections are named then it will merge the data from the
input connection under as connection name. For example if the connection name is "Personal data" then the merged data
will be:

```
{
  "Personal data": {
    ...payload
  }
}
```

If the connections are not named then data form incommin connection will be copied available under the connection id
key. 

# Merged data output reshaping

Joint data can be reshaped. 

Here is an example of reshape template.

```
{
  "some-data": {
    "key": "value",             // This is static value
    
    "value": "profile@id",      // Reads value from profile 
                                // and saves it in object 
                                // value key
                                
    "list": [1, "payload@data"],// Reads data value from 
                                // payload and saves it as 
                                // 2nd element of list
                                
    "event": "event@..."        // Saves in event all data 
                                // from event.
  }
}
```

Notice that some parts of this object reference data with dot notation. The data will be replaced be
the referenced data.

Let'ss assume that the merged payloads look like this:

```json
{
  "data": {
        "name": "John",
        "age": 26
      },
  "edge": {
    "test": 1
  }
}
```

then the result after data reshaping with the following template:

```
{
  "some-data": {
    "key": "value",
    "value": "profile@id"  
    "list": [1, "payload@data"] 
    "event": "event@..."
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