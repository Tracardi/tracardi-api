# What is the syntax of IF plugin condition

Here are some examples of IF action plugin conditions.

1. Simple condition with equals operator:

```
payload@field == "value"
```

2. Complex condition with AND:

```
(payload@field1 == "value1" AND payload@field2 != "value2")
```

3. Complex condition with OR:

```
(payload@field1 > 10 OR payload@field2 <= 5)
```

4. BETWEEN condition:

```
payload@age BETWEEN 18 AND 30
```

5. IS NULL condition:

```
session@user_id IS NULL
```

6. EXISTS condition:

```
profile@email EXISTS
```

7. NOT EXISTS condition:

```
memory@key NOT EXISTS
```

8. Compound value in a function:

```
event@timestamp > datetime(2023-01-01T00:00:00)
```

9. Empty condition:

```
flow@details EMPTY
```

10. Complex condition with nested parentheses:

```
(payload@field1 == "value1" AND (payload@field2 != "value2" OR payload@field3 > 0))
```

11. Complex condition that uses data functions.

```
(
    payload@age > 18 AND 
    (
        event@event_type == "click" OR 
        event@properties.action == "add_to_cart"
    ) AND 
    (
        profile@data.pii.age > 25 AND 
        (
            event@action == "purchase" OR 
            event@properties.action == "add_to_cart"
        )
    )
) OR (
    (
        payload@quantity BETWEEN 10 AND 50 OR 
        payload@timestamp BETWEEN 1631233200 AND 1631319600
    ) AND 
    (
        payload@description IS NULL OR 
        event@type IS NOT NULL
    ) AND 
    (
        event@properties.location EXISTS AND 
        profile@address NOT EXISTS
    )
) AND (
    (
        memory@notes EMPTY OR 
        payload@items NOT EMPTY
    ) AND 
    (
        payload@keywords CONTAINS "technology" OR 
        event@tags CONTAINS "important"
    )
) AND (
    (
        payload@name STARTS WITH "John" OR 
        event@description ENDS WITH "exciting event"
    ) AND 
    (
        event@participants[0] == "Alice" OR 
        event@ratings[2] >= 4.5
    )
) AND (
    now("europe/warsaw") > datetime("2021-01-01 00:00:00") AND 
    now("europe/london") < now.offset(payload@time, "+700 days")
)
```

12. CONTAINS Condition (contains string):

- Check if keywords in payload contain "technology":
```
  payload@keywords CONTAINS "technology"
```

- Check if event tags contain the word "important":
```
  event@tags CONTAINS "important"
```

13. STARTS WITH/ENDS WITH String Conditions:

- Check if payload name starts with "John":
```
  payload@name STARTS WITH "John"
```

- Check if event description ends with "exciting event":
```
  event@description ENDS WITH "exciting event"
```

Remember, these examples follow the syntax you provided and assume that the specified fields like `payload@keywords`
, `event@tags`, `payload@name`, and `event@participants[0]`, etc. exist in the data structure you're working with.
