# IF Action

If you want your flow to perform some conditional operation use this node. 

# Language

This node uses a language very similar to SQL conditionals. It also uses dotted path notation to access the data.
All fields must contain a source and a path to value e.g:

```
profile@traits.public.pii.name
```

This means the value *traits.public.pii.name* from profile will be used in the conditional statement.

# Language grammar

The following grammar rules define expression syntax in [If node].

```
expr:
  | expr OR (expr AND expr)
  | expr AND (expr OR expr)
```

that means that expressions with similar operators e.g. OR must be in brackets. The following conditional statement is forbidden:

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

Each condition consist of a field, operator, and value. An operator is used to manipulate individual data items and return a result.
Operators are represented by special characters or by keywords. List of operators is available below.

*Example*

```
payload@numberOfPurchases == 1
```

This example will trigger True port on the [IF node] if *numberOfPurchases* in payload equals 1

Operations can be joined by AND/OR. 

*Example*

```
payload@numberOfPurchases == 1 and payload@title == "Title"
```

This example will trigger True port on the [IF node] if *numberOfPurchases* in payload equals 1and *title* in payload 
equals "Title".

There are other operators possible like:

* less then (<)
* greater then (>)
* less or equal then (<=)
* greater or equal then (>=)
* not equal (!=)
* exists (*fieldname* EXISTS)
* not exists (*fieldname* NOT EXISTS)

# Value types

In the example:

```
payload@numberOfPurchases == 1 and payload@title == "Title"
```

Field *payload@numberOfPurchases* is considered an integer number while *payload@title* is considered a string.

# Troubleshooting

When you compare date you must pay attention to dates types. There are dates that are time zone aware (offset-aware)
and dates that are not aware of time zone. You can not compare them.

```
can't compare offset-naive and offset-aware datetimes
```

# Time functions

The following time functions are available:

* now()
* utcnow()
* datetime("<value>"), e.g datetime("2021-01-01 00:00:00")
* datetime(<field>), e.g datetime(profile@maetadata.time.insert)
* now("<time_zone>"), e.g. now("europe/warsaw")
* now.offset("europe/warsaw", "+700 days")
* now.offset(payload@time, "+700 days")