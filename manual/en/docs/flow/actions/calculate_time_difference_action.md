# Calculate Time Difference Plugin

This plugin calculates the time difference between two dates. 

## Config

The plugin takes two dates. 


* 1st date or path to date - this is a reference date, for example, *event@metadata.time.lastVisit*. 
* 2nd date or path to date

Dates can be in the following formats
* **now** - the time of workflow execution
* **date** - correct values are for example *2021-03-14* or *Aug 28 1999*. For more information about correct formats, check https://dateutil.readthedocs.io/en/stable/parser.html
* **path** - This one takes a path to date, e.g. *event@metadata.time.lastVisit*

## Output

This plugin returns time difference information on port ```time_difference```.
The returned time difference is ___always___ in form of an object with the following information:

```
{
    "seconds": <number-of-seconds>,
    "minutes": <number-of-minutes>,
    "hours": <number-of-hours>,
    "days": <number-of-days>,
    "weeks": <number-of-weeks>
}
```
These values can be floats.