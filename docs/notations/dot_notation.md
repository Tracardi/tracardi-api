# Dot notation

Dot notation is a way to access data in internal state of workflow. It is a standard 
way to reference data in Tracardi. It is used across many places in Tracardi such as 
plugins, destinations, etc. 

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
* memory

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
    `profile@data.name` then the result is the typed value, in this example `profile.data.name`. That means that any 
    value that is not a valid dot notation will be returned as is.

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

If you would like to retrieve a sub-object form some bigger object. For example everything below __key__. (see below).

```json
{
   "key": {
        "data": "value"
   }
}
```

Then you need to use the following dot notation:

```bash
profile@key #(1)
```

1. Return everything below __key__. The result will be ```{"data": "value"}```

## Path to array items

## Arrays

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


## Object with spaces in the keys

There are rare cases when you have an object with the keys that contain spaces.

```json title="Example"
{
   "key": {
        "My key with spaces": "value"
   }
}
```

To access this data you will need to use the following dot notation:

```bash
profile@key["My key with spaces"]
```

!!! Tip

    Also objects embeded inside arrays can be retrieved the same way. For exampel ``` profile@key.0["My key with spaces"] ```

# Read also about:

Notations that use dot notation:

* [Templates](templates.md)
* [Object templates](object_template.md)
* [Logic notation](logic_notation.md)

---
This documentation answers the following questions:

* What is dot notation?
* What is the purpose of dot notation in Tracardi?
* What are the available sources for dot notation in Tracardi?
* What is the format of dot notation in Tracardi?
* What is the warning associated with dot notation in Tracardi?
* How can a part of data be accessed using dot notation in Tracardi?
* How can items in an array be accessed using dot notation in Tracardi?
* Can objects embedded inside arrays be retrieved using dot notation in Tracardi?
* How can I access profile data in tracardi?
* How can I access event data in tracardi?
* How can I access session data in tracardi?
