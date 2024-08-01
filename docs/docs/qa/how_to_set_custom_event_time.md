# How to set custom event time in API payload?

To set a custom date for an event sent to Tracardi, you need to populate the `time` field within the event payload.
The `time` field can include attributes such as `insert`, `create`, and `update` to provide specific timestamps for the
event. Here's a step-by-step guide on how to set these custom timestamps.

### Event Payload Structure

The event payload consists of the following attributes:

- **type**: The type or category of the event (e.g., "page-view").
- **time**: Timestamp information for the event, which includes `insert`, `create`, and `update` attributes.
- **properties**: A dictionary of properties associated with the event.
- **options**: Additional options for the event.
- **context**: Additional context data for the event.
- **tags**: Tags associated with the event.

### Time Attribute Structure

The `time` attribute provides timestamp information and can include the following attributes:

- **insert**: The timestamp of the event insertion (default is the current UTC datetime).
- **create**: The timestamp of the event creation.
- **update**: The timestamp of the event update.

### Example: Setting Custom Dates in Event Payload

Here's an example of how to set custom dates in the event payload using the Tracardi JavaScript tracker:

```javascript
// Tracardi tracker initialization
const options = {
    tracker: {
        url: {
            script: 'http://your-tracardi-url/tracker',
            api: 'http://your-tracardi-url'
        },
        source: {
            id: "<your-event-source-id>"
        }
    }
};

// Define your custom event payload with custom dates
const customEventPayload = {
    "type": "custom-event-type",
    "time": {
        "insert": "2024-05-01T12:00:00Z",  // Custom insert time in ISO 8601 format
        "create": "2024-05-01T10:00:00Z",  // Custom create time in ISO 8601 format
        "update": "2024-05-01T11:00:00Z"   // Custom update time in ISO 8601 format
    },
    "properties": {
        "customProperty": "customValue"
    }
};

// Send the custom event with the custom dates
window.tracker.track("custom-event", customEventPayload);
```

### Explanation

1. **Tracker Initialization:**
   Initialize the Tracardi tracker with the correct script and API URLs, and your event source ID.

2. **Custom Event Payload:**
   Create an object for your custom event payload. The `time` field includes the `insert`, `create`, and `update`
   attributes with custom dates in ISO 8601 format. The `properties`, `options`, `context`, and `tags` fields provide
   additional event details.

3. **Send the Event:**
   Use `window.tracker.track` to send the event to Tracardi. The first parameter is the event type, and the second
   parameter is the payload that includes the custom dates.

This approach ensures that the event sent to Tracardi includes the custom timestamps you specified, allowing for
accurate temporal representation within your event tracking system. Make sure to replace placeholders
like `<your-event-source-id>` and `http://your-tracardi-url` with actual values relevant to your Tracardi instance.