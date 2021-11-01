# Notations 

Tracardi uses different types of notations to access data and define logic.

## Dot notation

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

The full access dot notation notation is *profile@key.data*.

## Path to part of data

There is also a way to access a part of data. 

A path like *profile@key* will return:

```json
{
  "data": "value"
}
```

To access all data from profile type *profile@...*.

# Logic notation

Logic notation is the way in which logical concepts and their interpretations 
are expressed in natural languages. Tracardi uses notation similar SQL.

## Syntax

The following grammar define logic expression syntax.

```
expr:
  | expr OR (expr AND expr)
  | expr AND (expr OR expr)
```

that means that expressions with similar operators e.g. OR must be in brackets. 
The following conditional statement is forbidden:

```
field1=1 AND field2=2 OR field3=3
```

correct statement is either:

```
field1=1 AND (field2=2 OR field3=3)
```

or

```
(field1=1 AND field2=2) OR field3=3
```

There is no auto resolution of priority operations

## Condition resolution

Each condition consist of a field, operator, and value. An operator is used to 
manipulate individual data items and return a result. 
Operators are represented by special characters or by keywords. List of operators is 
available below.

*Example*

```
payload@numberOfPurchases == 1
```

This example will return true if *numberOfPurchases* in payload equals 1.
Fields are in a dot notation please see documentation for *dot notation*.

Operations can be joined by AND/OR. 

*Example*

```
payload@numberOfPurchases == 1 and payload@title == "Title"
```

This example will trigger True if *numberOfPurchases* in payload equals 1and *title* in payload 
equals "Title".

There are other operators possible like:

* less then (<)
* greater then (>)
* less or equal then (<=)
* greater or equal then (>=)
* not equal (!=)
* exists (*field_name* EXISTS)
* not exists (*field_name* NOT EXISTS)

## Value types

In the example:

```
payload@numberOfPurchases == 1 and payload@title == "Title"
```

Field *payload@numberOfPurchases* is considered an integer number while 
*payload@title* is considered a string.

