# Calculate Time Diff Plugin

This plugin calculates time difference between two dates. 

## Config
Plugin takes reference date (field Reference date) and so called 'now date' (Second date). Both can be in one of following formats:
- Now - it's just the moment of running workflow, correct value in date field for this format is just ```now```.
- Date - that one is one specific date given by user. Correct values are for example ```2021-03-14``` or ```Aug 28 1999```. 
For more specific information about correct formats, check https://dateutil.readthedocs.io/en/stable/parser.html
- Path - This one takes path to date.

## Output
This plugin returns time difference information on port ```time_difference```.
Time difference information is ___always___ in form of:
```
{
    "seconds": <number-of-seconds>,
    "minutes": <number-of-minutes>,
    "hours": <number-of-hours>,
    "days": <number-of-days>,
    "weeks": <number-of-weeks>
}
```
These numbers are always integers since they are rounded down.
They always represent the same time range, just expressed with different units.
So, for example, we can have 82 hours and 3 days in same result, because 87 hours is 3 ___full___ days and 15 hours, but 
we ignore these 15 hours, because we return floor value from division.