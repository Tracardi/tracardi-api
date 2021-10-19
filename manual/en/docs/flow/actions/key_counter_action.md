# Key counter

This plugin counts key strings. Key string provided in configuration will be treated as an information 
to increase the value of a key in profile. For example if the key equals to `['a','b','a']` then the 
key count equals to `{"a":2, "b":1}`. 

This plugin can be used for simple statistics e.g. count how many user visited us on mobile device vs other devices
like desktop or tablet.

# Configuration

```json
{
  "key": "desktop",
  "save_in": "profile@stats.counters.MobileVisits"
}
```

* `key` may be a string or a list of strings. Also, a dot notation can be used to access data.
* `save_in` point to data in profile that will hold the information on key counts. It should be empty object `{}` or a key-value object.

*Example*

```json
{
  "key1": 10,
  "key2": 20
}
```

## Examples

Example of configuration with dot notation in `key` and `save_in`

```json
{
  "key": ["event@session.context.browser.agent", "event@session.context.browser.agent.string"],
  "save_in": "profile@stats.counters.visits_origins"
}
```