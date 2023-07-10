# Add Empty Session

Adds a new session to the event. An empty session is created with a random ID.

## Version

This documentation is for version 0.7.0 of the plugin.

## Description

The AddEmptySessionAction plugin is used to add an empty session to the event. It creates a new session with a random ID and assigns it to the event. The session is also saved in the database for future reference. This plugin is typically used in workflows where session data is required.

The plugin performs the following steps:

1. Generates a random ID for the session.
2. Creates a new session object with the generated ID.
3. Assigns the session to the event.
4. Updates the event's session metadata with the session ID, start time, and duration.
5. Updates the event's operation to indicate that it has been modified.
6. Sets the "saveSession" option in the tracker to True.
7. Returns the input payload.

Example output:

```json
{
  "payload": {
    "someData": "value",
    "session": {
      "id": "a1b2c3d4e5f6",
      "start": "2023-07-10T12:00:00Z",
      "duration": 3600
    }
  }
}
```

# Inputs and Outputs

- Input: This plugin takes the payload object as input.
- Output: This plugin returns the input payload.

# Configuration

This plugin does not require any configuration.

# JSON Configuration

```json
{}
```

# Required resources

This plugin does not require external resources to be configured.
