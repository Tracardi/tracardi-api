# Add Empty Profile

This plugin adds an empty profile to the event. An empty profile is created with a random ID and can be used to store information about a user.

# Version

Version 0.8.0

## Description

The Add Empty Profile plugin adds an empty profile to the event. It creates a new profile with a random ID and sets it as the profile for the event. Additionally, it updates the metadata of the event and sets the `profile_less` flag to `False` to indicate that a profile is associated with the event. The plugin also updates the execution graph to include the new profile.

If configured, the plugin can also create a new session for the profile. The session ID is set in the tracker payload and can be used by other plugins in the workflow.

## Inputs and Outputs

### Inputs

- **payload**: Accepts a payload object.

### Outputs

- **payload**: Returns the input payload.

## Configuration

- **New session**: Specifies whether to create a new session for the profile. The available options are:
  - **If not exists**: Creates a new session only if a session does not already exist.
  - **Always**: Always creates a new session.
  - **Never**: Does not create a new session.

## JSON Configuration

Example JSON configuration for the Add Empty Profile plugin:

```json
{
  "session": "always"
}
```

## Required resources

This plugin does not require any external resources to be configured.

## Errors

No errors are documented for this plugin.