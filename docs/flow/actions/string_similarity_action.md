# String similarity

This plugin checks similarity between two strings according to similarity algorithms.

# Configuration

Example:

```json
{
   "first_string": "event@properties.some_value1",
   "second_string": "event@properties.some_value2",
   "searching_algorithm": "Levenshtein"
}
```

# Input

This plugin takes payload as input

# Output

Returns result of the searching algorithm

Example:

```json
{
  "similarity": "1"
}
```