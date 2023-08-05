# Event Payload

The Event Payload is a component of the event tracker payload, which is used to track and record events. The complete
tracker payload follows this JSON structure:

```json
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID"
  },
  "context": {
    // Context data
  },
  "properties": {},
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      },
      "options": {
        // Event options
      },
      "context": {
        // Additional context data
      }
    },
    ...
  ],
  "options": {}
}
```

The specific part related to events is as follows:

```json
{
  "type": "event-type",
  "properties": {
    // Event properties
  },
  "options": {
    // Event options
  },
  "context": {
    // Additional context data
  }
}
```

The Event Payload consists of the following attributes:

| Attribute   | Type                   | Description                                     |
|-------------|------------------------|-------------------------------------------------|
| type        | str                    | Type or category of the event                   |
| time        | Optional[Time]         | Timestamp information for the event (optional)  |
| properties  | Optional[dict]         | Properties associated with the event (may be empty) |
| options     | Optional[dict]         | Additional options for the event (may be empty)     |
| context     | Optional[dict]         | Additional context data for the event (may be empty)|
| tags        | Optional[list]         | Tags associated with the event (optional)       |

The `Time` attribute, used within the `time` field, has the following structure:

The `Time` class provides timestamp information for the event, with the following attributes:

- `insert`: Optional[datetime] - The timestamp of the event insertion.
- `create`: Optional[datetime] - The timestamp of the event creation.
- `update`: Optional[datetime] - The timestamp of the event update.

If the `insert` attribute is not provided explicitly, it defaults to the current UTC datetime at the time of
instantiation.

## Usage

### Event type

Define event type as slug of its name. For example if the event type is `Page View` set `type` to `page-view`.

### Time

To send an event, you can populate the attributes described above according to your specific event data. If you wish to
override the current insert time, which represents the time of event collection, and instead use a custom time, you can
set the `time.insert` attribute to the desired date and time.

The same principle applies to the `create` and `update` attributes. If you want to provide custom timestamps for event
creation or update, you can set the corresponding values of `time.create` and `time.update` to the appropriate dates and
times.

By customizing the `time` attributes, you can have more control over the temporal aspects associated with the event,
ensuring accurate representation within your event tracking system.

### Properties

Event properties refer to specific attributes or characteristics that provide relevant details about an event. They
contain the actual data associated with the event and can vary depending on the nature of the event and the specific
requirements of the system or application. Here are some examples of what can be included as event properties:

1. User information: Information about the user involved in the event, such as user ID, username, email address, or any
   other relevant user identifiers.
2. Event parameters: Parameters or values that capture specific aspects of the event, such as quantity, price, duration,
   location, or any other measurable or meaningful attributes.
3. Status indicators: Flags or indicators that reflect the status or outcome of the event, such as success, failure,
   pending, or in-progress.
4. Metadata: Additional contextual information or metadata that provides further insights into the event, such as event
   source, event category, or any custom-defined metadata specific to the application or system.

Event properties serve to enrich the event data, allowing for a more detailed and meaningful representation of the event
within the system or application.

### Context

Event context encompasses supplementary information or data that offers a wider perspective on an event. It includes
pertinent details that contribute to a deeper comprehension of the event's surrounding circumstances. The specific
content of event context may vary based on the event's nature and the system or application requirements.

This additional data can take the form of metadata, providing context-specific information associated with the event.
Examples include contextual tags, event categories, or any custom contextual data tailored to the particular application
or system.

### Options

Event options provide additional instructions or directives related to the processing of an event. They can specify how
the event should be handled, what actions to take, or what data to return as a result of processing the event. Here are
some examples of what can be included as event options:

```
"options": {
        "saveEvent": false,
        "saveSession": false,
        "debugger": false
      },
```

Here is the description of the configuration options in a table format:

| Option      | Description                                                                                                                                               |
|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| saveEvent   | Determines whether the event should be saved or treated as ephemeral. If set to `false`, the event is processed but not permanently saved.                    |
| saveSession | Specifies whether the session associated with the event should be saved. If set to `false`, the session data will not be stored for this particular event. |
| debugger    | Controls the inclusion of debugger information in the event response. If set to `false`, debugger information will not be returned.                          |

### Tags

When choosing tags for a specific event, consider the event type, relevant attributes, business context, and analytical
needs. Use consistent and meaningful tags to categorize and organize events effectively.