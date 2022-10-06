# Key counter

This plugin counts key strings. Key string provided in configuration will be treated as an information to increase the
value of a key in profile. This plugin can be used for simple statistics e.g. count how many user visited us on mobile
device vs other devices like desktop or tablet.

## Examples

For example Lets assume the following configuration:

```json
{
  "key": "payload@value",
  "save_in": "payload@traits.public.counts"
}
```

if over time the value in payload (defined in config as payload@value) is equals to:

```
{"value": "a"}
{"value": "b"}
{"value": "a"}
```

or value in payload is a list of 

```json
[
  "a",
  "b",
  "a"
]
``` 

then the key count equals to

```json
{
  "a": 2,
  "b": 1
}
```

and will be saved in **payload@traits.public.counts**

If the payload values are:

```json
[
  {"key1": 1},
  {"key2": 2},
  {"key1": 2}
]
```

then the key will be increased by the provided value. Then *key1* + 1, *key2* + 2, and *key1* + 2. And the result will
be:

```json
{
  "key1": 3,
  "key2": 2
}
```

You may also want to pass data the following way:

```json

  {
    "key1": 1,
    "key2": 2
  }
```

This will also work and the result will be:


```json
  {
    "key1": 1,
    "key2": 2
  }
```

# Configuration

```json
{
  "key": "desktop",
  "save_in": "profile@stats.counters.MobileVisits"
}
```

Example of configuration with dot notation in *key* and *save_in*

```json
{
  "key": "event@session.context.browser.agent",
  "save_in": "profile@stats.counters.visits_origins"
}
```

Or with multiple key fields.

```json
{
  "key": [
    "event@session.context.browser.agent",
    "event@session.context.browser.agent.string"
  ],
  "save_in": "profile@stats.counters.visits_origins"
}
```

* *key* may be a string or a list of strings. Also, a dot notation can be used to access data.
* *save_in* point to data in profile that will hold the information on key counts. It should be empty object *{}* or a
  key-value object. *save_in* holds the original data that will be incremented.

