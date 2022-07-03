# Memory payload collector

This action node collects input payloads in a defined key inside memory object. Memory object is kept inside workflow
and can be references with `copy data` plugin or any dotted notation string, eg. `memory@defined_key`.

One node may be connected to nodes. This means that it will be executed as many times as there were nodes connected to
it. Each of them sends the result of its operation (payload). In order to collect data into one object, it is necessary
to combine them. The node "collect payloads" collects them and saves them in the memory object under the given key.

Two types of connection are possible.

List type. It allows you to see all incoming payloads in the list. e.g.

```json
{
  "my-key": [
    {"key":  "payload1"},
    {"key":  "payload2"},
    {"key":  "payload3"}
  ]
  
}
```

Dictionary type. It combines all incoming payloads into a dictionary type where the key for each payload is the name of
the connection (called sometimes graph edge) it came from, e.g.

```json
{
  "my-key": {
    "edge-name1":  {"key": "payload1"},
    "edge-name2":  {"key":  "payload2"},
    "edge-name3":  {"key":  "payload3"}
  }
  
}
```

# Advanced Configuration

Example

```json
{
  "name": "my-key",
  "type": "list"
}
```

* name - the name (key in memory object) that will hold the collected payloads.  
* type - type of collection. Possible values: "list", "dict"