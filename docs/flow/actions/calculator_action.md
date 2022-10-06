# Calculator

This plugin performs simple operations such as add, subtract, divide, and multiply. Arguments of those operations may be
values from payload, profile, etc. The result is returned as an object of new values.

Each operation must be in separate row. Operations may share variables.

*Example 1*

```
profile@traits.private.interests.sports =  profile@traits.private.interests.sports / payload@time_passed
```

This calculation will divide the value from profile that is located in **traits.private.interests.sports** by the number
provided in payload (time_passed). Value of time_passed can be a time that passed from the last visit. The above
equation will return the following result.

```json
{
  "result": <some-value>,
  "variables": {}
}
```

*Example 2 - variables*

```
decay_rate = 2
result.value = profile@traits.private.interests.sports / decay_rate
```

This simple calculation assigns value to variable decay_rate. Then uses this value to compute result.value. This
equation will return the following result.

```json
{
  "result": <some-value-equal-to-last-operation-result.value>,
  "variables": {
    "decay_rate": 2,
    "result": {
      "value": <some-value-equal-to-last-operation-result.value>
    }
  }
}
```

This way you can construct object that have different values that are calculated and assigned to variables. Of course
the variable ca be assigned to profile, session, etc. This is the last example with variable result.value assingned to
profile@traits.private.interests.sports

```
decay_rate = 2
result.value = profile@traits.private.interests.sports / decay_rate
profile@traits.private.interests.sports = result.value
```

# Compound calculations

Calculations may have several operations.

```
a = 1 + 2 / 3
b = (1 + 2) / 3
c = a + b
```

The result of this calculation is:

```json
{
  "result": 2.6666666666666665,
  "variables": {
    "a": 1.6666666666666665,
    "b": 1,
    "c": 2.6666666666666665
  }
}
```

Each number can be replaced by variable or a field from profile, event, etc.

# Negative values

```
event@counter = 1
-event@counter
```

The result of this operation is:

```json
{
  "result": -1,
  "variables": {}
}
```

And the event@counter equals 1.
