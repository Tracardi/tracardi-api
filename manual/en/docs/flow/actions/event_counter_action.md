# Event counter

This plugin reads how many events of defined type were triggered within defined time.

## Configuration

*Example*
```
{
 "event_type": "page-view",
 "time_span": "-15m"
}
```

* `event_type` - value should be a string containing type of event that user wants to count.
* `time_span` - should be a string containing time span which user wants to search in, for example using ```"-1h30min"``` as ```"time_span"``` on 1st March 2022, 1:00 (a.m.) results in searching through all events that happened between 28th February 2022, 23:30 and 1st March 2022, 1:00 (a.m.). Presence of ```"-"``` sign in timeSpan does not matter, since it is stripped anyway. For more details, visit [pytimeparse library documentation](https://pypi.org/project/pytimeparse/).


## Output

Plugin outputs number of found events.

Example:
```
{
    "events" : 39
}
```
