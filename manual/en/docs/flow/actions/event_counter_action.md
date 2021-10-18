# Event Counter Plugin

## Input
Plugin takes input (as arg payload).\
Input template/example:
```
{
 "eventType": "page-view",
 "timeSpan": "-15m"
}
```

```"eventType"``` value should be a string containing type of event that user wants
to count.

```"timeSpan"``` should be a string containing time span which user wants to search in,
for example using ```"-1h30min"``` as ```"timeSpan"``` on 1st March 2022, 1:00 (a.m.) results in
searching through all events that happened between 28th February 2022, 23:30 and
1st March 2022, 1:00 (a.m.).
Presence of ```"-"``` sign in timeSpan does not matter, since it is stripped anyway.
For more details, visit [pytimeparse library documentation](https://pypi.org/project/pytimeparse/).


## Output
Plugin outputs instance of Result class, with ```"payload"``` as ```port```  and an integer representing number of
events with selected type found in given ```"timeSpan"```, assigned to Result's ```value``` parameter.

Example:
```
port='payload'
value=39
```
