# Value mapping plugin

This plugin works like a value switch. Unlike if-then and if-then-else statements, the switch statement can have a
number of possible execution paths. The statement value is compared to all the defined key values. If it matches the
value the corresponding value is returned.

## Input

This plugin takes any payload object as input.

## Output

This plugin outputs one of values defined in config if it matches its key in the provided set of key-value pairs. If
none of the values are equal to statement value **null** is returned. 


## Configuration example

Configuration takes a __value__ and a set of data defined in __switch__ property.

```json title="Example"
{
  "value": "<statement-value>",
  "switch": {
    "payload@xyz": "value1",
    "key1": "profile@abc",
    "key2": "value2"
  }
}
```

Value contains a statement value. It will be compared with all the key values defined in a "switch". In this example:
value referenced by "payload@xyz", key1, key2. If statement value is also a reference to value for example profile@id
then it will be evaluated first and the referenced value will be used as a statement value. 

In the above case, when the field specified in **value** has the same value as
value referenced by **payload@xyz**, then **value1** will be returned. If **value** is equal to **key1**, then value from field **
profile@abc** will be returned, etc.

## Result example

```json
{
  "value": "value2"
}
```



