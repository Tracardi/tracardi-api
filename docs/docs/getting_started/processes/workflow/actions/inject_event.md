# Inject Event

Inject Event is a Plugin that allows you to add an event to the payload by providing the event id. The event is directly
loaded into the payload, augmenting the data as it passes through the workflow.

# Version

The version of the plugin used for this documentation is 0.6.0.1.

## Description

The Inject Event plugin enables you to add an event into the payload (the data structure that carries content for the
workflow). When the plugin is run, it loads the event associated with the provided event id into the current payload. If
the event is not found, a warning is logged. The modified payload, containing the newly added event, is then returned.

Please note that Inject Event can start the workflow.

# Inputs and Outputs

The plugin accepts one input - a payload:

Example:

```
{
  "payload": {
    "data": "Any data you need to pass to the plugin"
  }
}
```

The plugin also outputs the modified payload:

Example:

```
{
  "payload": {
    "data": "Any data you need to pass to the next plugin",
    "event": "Loaded event data"
  }
}
```

The __payload__ output is the input payload enriched with the event data related to the provided id.

# Configuration

The plugin has one configuration parameter:

- __event_id__: This required parameter specifies the id of the event you want to add to the payload.

# JSON Configuration

Here is an example of the JSON configuration:

```
{
  "event_id": "123456"
}
```

Please replace "123456" with the actual id of the event you want to inject into your workflow.

# Required resources

This plugin does not require external resources to be configured.

# Errors

If the specified "event_id" does not exist in the event database, the following warning will be logged: "Event id XXX
does not exist.". In this case the plugin continues executing and returns the input payload unchanged.