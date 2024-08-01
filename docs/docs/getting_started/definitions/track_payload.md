# Tracker Payload

Tracker payload refers to the comprehensive data structure sent to the Tracardi system to record an
event. This payload includes all the necessary information to track and analyze customer interactions. Here's a detailed
breakdown of the track payload:

## Structure of the Track Payload

The payload typically follows this JSON structure:

```json title="Example of tracker payload"
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "profile": {
    "id": "profile-id"
  },
  "context": {
    // Context data
  },
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
    }
  ],
  "options": {}
}
```

### Key Components of the Track/Tracker Payload

1. **Source**:
    - **id**: The ID of the source from which the event originates. This must match the event source defined in
      Tracardi.

2. **Session**:
    - **id**: The ID of the session. This ID is typically generated on the client side using UUID4 and should change
      with each new user visit.

3. **Profile**:
    - **id**: The ID of the user's profile. If it's the first visit, this may not be included, and Tracardi will
      generate a new profile ID.

4. **Context**:
    - Additional data that provides context about the event, such as device information, browser type, or location. This data is stored in the [session](../components/session.md).

6. **Events**:
    - **type**: The type of event, such as "page-view" or "purchase-order".
    - **properties**: Data specific to the event type.
    - **options**: Optional parameters to control event processing, such as immediate firing or beacon mode.
    - **context**: Additional context data for the event, such as tags or additional metadata.

7. **Options**:
    - Global options for the payload, such as whether to save the session or event, or to enable async storage.

### Example Payload

A minimal payload might look like this:

```json title="Minimal payload"
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "Home Page"
      }
    }
  ]
}
```

!!! Important Notes

    **Session and Profile IDs**: These are crucial for linking events to the correct session and user profile. The session  ID should be unique per visit, while the profile ID remains consistent across all visits.
    **Context and Properties**: These fields provide additional metadata and attributes that enrich the event data, allowing for more detailed analysis.
