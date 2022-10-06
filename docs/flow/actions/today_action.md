# Today plugin

Plugin read a time in a give time zone.

# Configuration

```json
{
  "timezone": "session@context.time.tz"
}
```

Time zone can ba a path to timezone data or a plain text. Time zone must be in a format of "country/city".

See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for detailed list of timezones.

# Output

```json
{
  "utcTime": "2021-10-25T09:13:29.341421",
  "timestamp": 1635153209.341412,
  "server": {
    "dayOfWeek": "monday",
    "day": 25,
    "month": 10,
    "year": 2021,
    "week": 1,
    "hour": 5,
    "minute": 13,
    "second": 29,
    "ms": 341395,
    "time": "05:13:29.341395",
    "fold": 0,
    "iso": "2021-10-25T05:13:29.341395-04:00"
  },
  "local": {
    "dayOfWeek": "sunday",
    "day": 24,
    "month": 10,
    "year": 2021,
    "week": 1,
    "hour": 23,
    "minute": 13,
    "second": 29,
    "ms": 341395,
    "time": "23:13:29.341395",
    "fold": 0,
    "iso": "2021-10-25T23:13:29.341395-04:00"
  }
}
```