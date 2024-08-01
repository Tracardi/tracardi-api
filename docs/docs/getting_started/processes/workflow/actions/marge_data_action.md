# Merge data

The plugin can combine data from two data schemas. This is especially useful in situations where we want to add a new set of data to the existing one. For example, a new set of features for an existing entity. Or when we want to combine profile and event data.

The plugin works in such a way that we indicate the source data and the data that we want to combine. The source data is in the form of reference and the data that we want to add is passed in the form of an object. The object can be a schema with references to workflow data. For this purpose, we use an object template - more about the object template can be found in the documentation.

The output of this plugin is the combined output of the plugin.

# Configuration

The plugin requires:

- __source__ - a reference to input data, e.g. __profile@traits.public__
- __data__ - data to be merged. An object with data: __{"name": "Bill"}__
- __connection__ - a method how to combine the data. The available methods are:
  - __override__ - overwrite data in case of data conflict
  - __merge__ - combine data in case of conflict in array of all data

# Example

Lets assume that our profile has the following traits:

```json
{
   "public": {
       "name":"William",
       "surname": "Gates",
       "age": 70
    }
}
```

We reference it in configuration as a source: __profile@traits__

Then we define our data to merge: 

```json
{
  "public": {
     "name": "Bill"
  },
  "private": {
     "location": "LA, USA"
  }
}
```

After merging we get the follwin result.

For override method:

```json
{
  "public": {
     "name": "Bill",
     "surname": "Gates",
     "age": 70
  },
  "private": {
     "location": "LA, USA"
  }
}
```

For merge method:

```json
{
  "public": {
     "name": ["Bill", "William"],
     "surname": "Gates",
     "age": 70
  },
  "private": {
     "location": "LA, USA"
  }
}
```

Notice that if there are different values for the same field, e.g. for the name field, one is "Bill", the second time it is "William", then the data will be combined and we will get a value name = ["Bill", "William"] if merge method is selected.
