Filtering is used in Tracardi to limit the number of event, profiles, etc. on the page. It uses a query parser that
allows to define the rules of filtering.

The query string is parsed into a series of terms and operators. A term can be a single word a phrase, surrounded by
double quotes "quick brown" which searches for all the words in the phrase, in the same order.

Operators allow you to customize the search.

## Operators

You can specify fields to search in the query syntax:

* Find the records where status field contains active
    ```
    status:active
    ```

* where the event.type field contains __page-view__  or __purchase__

    ```
    event.type:(page-view OR purchase)
    ```

    Remember the operators like OR, AND must be uppercase.

* where the __event.properties.product__ field contains the exact phrase "Nike sneakers"

    ```
    event.properties.product:"Nike sneakers"
    ```

* where the profile first name field contains Alice (note how we need to escape the space with a backslash)

    ```
    profile.pii.first\ name:Alice
    ```

* where any of the fields __book.title__, __book.content__ or __book.date__ contains quick or brown (note how we need to escape the
    * with a backslash):

    ```
    book.\*:(quick OR brown)
    ```

* where the field title has any non-null value:

    ```
    _exists_:title
    ```


* where the field title does not exist:

    ```
    NOT _exists_:title
    ```
    or
    ```
    !_exists_:title
    ```
    
  
## Wildcards

Wildcard searches can be run on individual terms, using ? to replace a single character, and * to replace zero or more
characters:

```
qu?ck bro*
```

Be aware that wildcard queries can use an enormous amount of memory and perform very badly just think how many terms
need to be queried to match the query string "a* b* c*".

!!! Warning

    Allowing a wildcard at the beginning of a word (eg "*ing") is particularly heavy, because all terms in the index 
    need to be examined, just in case they match. Leading wildcards are disabled.

## Regular expressions

Regular expression patterns can be embedded in the query string by wrapping them in forward-slashes ("/"):

```
name:/joh?n(ath[oa]n)/
```

## Fuzziness

You can run fuzzy queries using the ~ operator:

```
quikc~ brwn~ foks~
```

The query uses the Damerau-Levenshtein distance to find all terms with a maximum of two changes, where a change is the
insertion, deletion or substitution of a single character, or transposition of two adjacent characters.

The default edit distance is 2, but an edit distance of 1 should be sufficient to catch 80% of all human misspellings.
It can be specified as:

```
quikc~1
```

!!! Warning "Avoid mixing fuzziness with wildcards"

    Mixing fuzzy and wildcard operators is not supported. When mixed, one of the operators is not applied. For example,
    you can search for app~1 (fuzzy) or app* (wildcard), but searches for app*~1 do not apply the fuzzy operator (~1).

## Ranges

Ranges can be specified for date, numeric or string fields. Inclusive ranges are specified with square brackets 
[min TO max] and exclusive ranges with curly brackets {min TO max}. By default, when you filter by query ranges in 
filtering box (right to the filter textbox) are disabled. You can define ranges as query.


### Examples

* All days in 2012:
  ```
  date:[2012-01-01 TO 2012-12-31]
  ```
  
* Numbers 1..5

  ```  
  count:[1 TO 5]
  ```

* Tags between alpha and omega, excluding alpha and omega:

  ```
  tag:{alpha TO omega}
  ```
  
* Numbers from 10 upwards

  ```
  count:[10 TO *]
  ```

* Dates before 2012

  ```
  date:{* TO 2012-01-01}
  ```

* Ranges with one side unbounded can use the following syntax:

  ```
  age:>10
  age:>=10
  age:<10
  age:<=10
  ```


## Boolean operators

When filtering all terms are optional, as long as one term matches the record is returned. A search for __foo bar baz__
will find any document that contains one or more of __foo or bar or baz__.

There are also boolean operators which can be used in the query string itself to provide more control.

The operators are + (this term must be present) and - (this term must not be present). All other terms are optional. 

For example, this query:

```
quick brown +fox -news
```

states that:

* fox must be present
* news must not be present
* quick and brown are optional their presence increases the relevance

### And, or, not

The boolean operators AND, OR and NOT (also written &&, || and !) are also supported but beware that they do not honor
the usual precedence rules, so parentheses should be used whenever multiple operators are used together. For instance 
the previous query could be rewritten as:

```
((quick AND fox) OR (brown AND fox) OR fox) AND NOT news
```


