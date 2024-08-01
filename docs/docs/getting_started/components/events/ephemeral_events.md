In Tracardi, ephemeral events are temporary events that are processed without being permanently stored in the system.
These events are useful for scenarios where real-time processing is required, but long-term storage of the event data is
unnecessary. Here’s a detailed overview of ephemeral events in Tracardi:

### Characteristics of Ephemeral Events

1. **Temporary Nature**: Ephemeral events are processed in real-time but are not saved to the Tracardi database.
2. **Real-Time Processing**: These events are typically used for workflows that need immediate action or decision-making
   based on the event data.
3. **Reduced Storage Load**: By not storing these events, Tracardi reduces the load on storage systems, which can be
   beneficial for high-frequency event scenarios.

### Use Cases for Ephemeral Events

- **Real-Time Personalization**: Triggering immediate changes to a webpage based on user interactions without storing
  the interaction data.
- **Dynamic Notifications**: Sending instant notifications or alerts based on specific user actions.
- **Temporary Data Handling**: Handling data that is only relevant for a short period and does not need to be stored for
  future analysis.

### Implementing Ephemeral Events

There are two main ways to configure events as ephemeral in Tracardi:

1. **Ephemeral Event Sources**:
    - When defining an event source, you can configure it to handle events ephemerally.
    - This ensures that all events coming from this source are processed without being stored.

2. **Event Payload Configuration**:
    - Within the event payload, you can set the `options` attribute with `saveEvent` set to `false`.
    - This configuration directs Tracardi to process the event without saving it.

### Example Configuration

Here’s an example of how to configure an event payload to be ephemeral:

```json
{
  "type": "page-view",
  "properties": {
    "url": "https://example.com",
    "title": "Example Page"
  },
  "options": {
    "saveEvent": false
  }
}
```

In this example, the `saveEvent` option is set to `false`, making this a temporary event that will be processed but not
stored.

### Benefits of Ephemeral Events

- **Performance**: By avoiding the overhead of storing events, the system can process events more quickly.
- **Scalability**: Reduces the storage requirements, allowing the system to handle a larger volume of events.
- **Cost Efficiency**: Lower storage costs as events are not retained long-term.

### Considerations

- **Data Persistence**: Since ephemeral events are not stored, any data or insights derived from these events will not
  be available for future analysis.
- **Workflow Design**: Workflows using ephemeral events should be designed to handle the event data immediately, as it
  will not be available later.

### Summary

Ephemeral events in Tracardi provide a way to handle real-time event processing without the need for long-term storage.
They are ideal for scenarios where immediate action is required, and the event data does not need to be preserved. By
configuring events or event sources as ephemeral, you can optimize the performance and scalability of your Tracardi
system.