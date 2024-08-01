# Ghost

This plugin adds labels to a Ghost member by matching their UUID (a unique identifier) with the corresponding profile in
Ghost's database.

# Version

This documentation is for version 0.9.0 of the plugin.

## Description

The Ghost plugin connects to your Ghost site to update a member's labels based on their UUID. Here's a step-by-step
description of how it works:

1. It first checks the configuration to ensure it has the necessary API key and member UUID.
2. The plugin generates a token to authenticate with the Ghost API.
3. It retrieves the member's details from Ghost using the provided UUID.
4. The plugin compares the member's current labels with the segments assigned to the profile in Tracardi.
5. If the labels and segments match, no update is needed, and it simply returns the current labels.
6. If there is a mismatch, the plugin updates the member's labels in Ghost to match the profile's segments in Tracardi.
7. The plugin then returns the updated labels and a response from the Ghost service.

# Inputs and Outputs

- **Inputs:** The plugin takes a payload object, which should include the member's UUID and potentially other data from
  Tracardi's internal state.
- **Outputs:** There are two possible outputs:
    - **Result:** Returns the member's labels after checking or updating them.
    - **Error:** Outputs an error message if the plugin encounters any issues during its execution.

This plugin does not initiate the workflow.

# Configuration

To configure the plugin, you need to provide:

- **Ghost Resource:** The resource ID and name where the Ghost API key is stored.
- **UUID:** The dot notation path to the member's UUID in the payload.

# JSON Configuration

```json
{
  "resource": {
    "id": "resource-id",
    "name": "Ghost Resource"
  },
  "uuid": "payload@member.uuid"
}
```

# Required resources

This plugin requires a configured resource in Tracardi that stores the Ghost API key.

# Event prerequisites

The plugin works with all event types and does not have specific requirements for the event to be synchronous.

# Errors

- **Could not split API key into id and secret:** This error occurs if the provided API key does not contain a colon (:)
  character, which is required to separate the ID and secret parts of the key.
- **Connection errors or response issues with Ghost API:** These are general errors that can occur if there is a problem
  with the network connection, the Ghost API is down, or the API responds with an unexpected result.
- **JWT token issues:** Errors related to generating the JWT token for authentication with Ghost, which could be due to
  incorrect API key parts or other token generation issues.

These errors are logged in Tracardi's console and returned in the error output port, indicating issues that need to be
addressed in the plugin's configuration or the network environment.