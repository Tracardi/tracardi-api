# How do I filter data? What query should I use to filer data?

To filter data in Tracardi prior version 0.8.2, you can use the query syntax provided by the platform. Here are some examples of how to
construct queries to filter data:

1. Search by a specific field value:

* To find records where the status field contains "active": status:active To find records where the event type field
  contains either "page-view" or "purchase": event.type:(page-view OR purchase)
* To find records where the event properties product field contains the exact phrase "Nike sneakers":
  event.properties.product:"Nike sneakers"
* To find records where the profile first name field contains "Alice": profile.data.pii.firstname:Alice. Please note the need to
  escape the space if in field name with a backslash.

2. Wildcard searches:

* You can use wildcard characters to replace single or multiple characters in a term. For example, qu?ck will match "
  quick" or "quack", and bro* will match "brown", "brother", etc.

3. Regular expressions:

* Regular expression patterns can be embedded in the query string using forward-slashes ("/"). For example, name:
  /joh?n(ath[oa]n)/ will match "john" or "jonathan".

4. Fuzzy queries:

* Fuzzy queries allow for approximate matches. Use the tilde (~) operator with a numeric value to specify the maximum
  number of changes allowed. For example, quikc~ brwn~ will match "quick brown" or "quack brown".

5. Ranges:

* Ranges can be specified for date, numeric, or string fields. Inclusive ranges are specified with square
  brackets [min TO max], and exclusive ranges with curly brackets {min TO max}. For example,
  date:[2012-01-01 TO 2012-12-31] will match all days in 2012.

6. Boolean operators:

* The boolean operators AND, OR, and NOT (also written as &&, ||, and !) can be used to combine multiple conditions.
  Parentheses should be used to specify the desired precedence. For example, (quick AND fox) OR (brown AND fox) OR fox)
  AND NOT news will match records that contain "quick" and "fox" or "brown" and "fox" or just "fox", but not "news".

For more information look for term `Data searching` in the documentation.

---
This document also answers the questions:
- How to search data in Tracardi?
- How to find data in Tracardi?
