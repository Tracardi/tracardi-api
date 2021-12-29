# Dot notation

Dot notation is a way to access data in internal state of workflow. It is a standard 
way to access data in Tracardi. It is used across many places in Tracari such as 
plugins, etc. 

## Example of dot notation

```
event@properties.name
```

Dot notation is build from *source* and *path to data*. Available sources are:

* profile
* event
* payload
* flow
* session

Path is a string of keys that indicate where the data is placed.

For example if your profile data looks like this

```json
{
   "key": {
        "data": "value"
   }
}
```

To access "value" your path will need to look like this: *key.data*.

The full access dot notation is *profile@key.data*.

!!! Warning

    If there is an error in dot notation or it is not in a right format e.g `profile.data.name` instead of 
    `profile@data.name` then the result of it is the typed value, in this example `profile.data.name`

## Path to part of data

There is also a way to access a part of data. 

A path like *profile@key* will return:

```json
{
  "data": "value"
}
```

To access all data from profile type:

```bash
profile@... #(1)
```

1. Return the whole profile object

## Path to array items


Items in array can be accessed like this. For the payload data:

```json
{
  "data": ["value1", "value2"]
}
```

accessor that get `value1` should look like this.

```
payload@data.0
```

!!! Tip

    Also objects embeded inside arrays can be retrieved the same way.

