# Logic notation

Logic notation is the way in which logical concepts and their interpretations 
are expressed in natural languages. Tracardi uses logic notation in segment configuration, IF plugin action,or other 
conditional statements.

## Syntax

The following grammar define logic expression syntax.

```
expr:
  | expr OR (expr AND expr)
  | expr AND (expr OR expr)
```

that means that expressions with similar operators e.g. OR must be in brackets. 

!!! Warning "Remember..."

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

Each condition consist of a __field, operator, and value__. An operator is used to 
manipulate individual data items and return a result. 
Operators are represented by special characters or by keywords. List of operators is 
available below.

``` title="Example"
payload@numberOfPurchases == 1
```

This example will return __true__ if *numberOfPurchases* in payload equals 1.
Fields are in a [dot notation](dot_notation.md).

Operations can be joined by AND/OR. 

``` title="Example"
payload@numberOfPurchases == 1 AND payload@title == "Title"
```

This example will return True if *numberOfPurchases* in payload equals 1 and *title* in payload 
equals "Title".

There are other operators possible like:

* less then (<)
* greater then (>)
* less or equal then (<=)
* greater or equal then (>=)
* not equal (!=)
* exists (*field_name* EXISTS)
* not exists (*field_name* NOT EXISTS)
* empty (*field_name* EMPTY)
* not empty (*field_name* NOT EMPTY)

## Value types

In the example:

``` title="Example"
payload@numberOfPurchases == 1 AND payload@title == "Title"
```

Field *payload@numberOfPurchases* is considered an integer number while 
*payload@title* is considered a string. 

!!! Warning

    Values of differnet types can not be compared. 

## Functions

Functions can be used to convert value, for example to certain types.

* now() - returns current date and time
* utcnow() - returns current UTC date and time
* datetime(*field_name*) - returns *field_name* field content as date and time
* now(*time_zone*) - returns current date and time with given *timezone* info
* now.offset(*offset*) - returns current date and time with given offset (e.g. -15m)
* now.timezone.offset(*timezone*, *offset*) - returns current date and time with given 
  *timezone* info with applied *offset*
* datetime.offset(*field_name*, *offset*) - returns *field_name* field content as 
  date and time with applied *offset*
* datetime.timezone(*field_name*, *timezone*) - returns *field_name* field content
  as date and time with *timezone* info
* now.timezone(*timezone*) - returns current date and time with given *timezone* info
* lowercase(*field_name*) - returns lowercased text value of *field_name*
* uppercase(*field_name*) - returns upper-cased text value of *field_name*
* datetime.from_timestamp(*field_name*) - returns date and time created from timestamp
  content of field *field_name*

