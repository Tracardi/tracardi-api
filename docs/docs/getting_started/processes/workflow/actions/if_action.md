# IF Action

The "If" plugin in Tracardi is a conditional action that allows you to selectively run a branch of the workflow based on a specified condition. This plugin evaluates the provided condition and returns the payload on the "true" port if the condition is met, or on the "false" port if the condition is not met.

## Plugin Configuration

The behavior of the "If" plugin is determined by the following configuration options:

- **Condition statement**: This configuration option allows you to provide a condition for the IF statement. If the condition is met, the payload will be returned on the "true" port; otherwise, the "false" port will be triggered.

- **Return value only once per condition change**: By enabling this option, the relevant port will be triggered only once per condition change. If the option is disabled, the flow will be stopped.

- **Expire trigger again after**: If the value is set to 0, the event will occur only once and will not be triggered again unless the conditions change. However, if a value greater than 0 is set, the event will be triggered again after the specified number of seconds, regardless of whether the conditions have changed or not.

- **Return input payload instead of True/False**: Enabling this option will return the input payload on the output ports if it is enabled; otherwise, True/False will be returned.

## Plugin Outputs

The "If" plugin has two output ports:

- **true**: If the defined condition is met, the payload will be returned on this port.

- **false**: If the defined condition is not met, the payload will be returned on this port.

# Condition syntax

This node uses a language very similar to SQL conditionals. It also uses dotted path notation to access the data.
All fields must contain a source and a path to value e.g:

```
profile@data.pii.name
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


# Examples

1. Simple Comparison:
   ```
   payload@age > 18
   event@event_type == "click"
   profile@is_verified == True
   memory@score >= 90
   ```

2. AND/OR Conditions:
   ```
   (payload@category == "electronics" AND payload@price <= 1000)
   (event@action == "purchase" OR event@properties.action == "add_to_cart")
   (profile@data.pii.age > 25 AND (event@action == "purchase" OR event@properties.action == "add_to_cart"))
   ```

3. BETWEEN Condition:
   ```
   payload@quantity BETWEEN 10 AND 50
   payload@timestamp BETWEEN 1631233200 AND 1631319600
   ```

4. IS NULL/IS NOT NULL Conditions:
   ```
   payload@description IS NULL
   event@user_id IS NOT NULL
   ```

5. EXISTS/NOT EXISTS Conditions:
   ```
   event@location EXISTS
   profile@address NOT EXISTS
   ```

6. EMPTY/NOT EMPTY Conditions:
   ```
   memory@notes EMPTY
   payload@items NOT EMPTY
   ```

7. CONTAINS Condition (contains string):
   ```
   payload@keywords CONTAINS "technology"
   event@tags CONTAINS "important"
   ```

8. STARTS WITH/ENDS WITH String Conditions:
   ```
   payload@name STARTS WITH "John"
   event@description ENDS WITH "exciting event"
   ```

9. Array Conditions:
   ```
   event@participants[0] == "Alice"
   event@ratings[2] >= 4.5
   ```

!!! Warning

    Please note that the examples provided above are just illustrations of how the conditions might look like within the
    given syntax. The actual conditions used will depend on the specific context and data structure being used.

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
* datetime(<field>), e.g datetime(profile@metadata.time.insert)
* now("<time_zone>"), e.g. now("europe/warsaw")
* now.offset("europe/warsaw", "+700 days")
* now.offset(payload@time, "+700 days")