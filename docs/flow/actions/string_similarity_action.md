# String similarity

This plugin checks similarity between two strings according to similarity algorithms.

# Configuration

Example:

```json
{
   "first_string": "event@properties.some_value1",
   "second_string": "event@properties.some_value2",
   "algorithm": "Levenshtein"
}
```

# Input

This plugin takes payload as input

# Output

Returns the result of similarity check.

Example:

```json
{
  "similarity": "1"
}
```

In this example 1 means full similarity