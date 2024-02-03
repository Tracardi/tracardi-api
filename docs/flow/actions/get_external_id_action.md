# Load Integration Id

This plugin helps in synchronizing profile IDs between Tracardi and external systems. If your profiles have identifiers
in external systems, this plugin allows you to retrieve the connection between these systems and update the Tracardi
profile with the external ID.

# Version

0.8.2

## Description

When executed, this plugin attempts to retrieve the integration ID(s) for the current profile based on the specified
external system name. The system name is processed by lowercasing and replacing spaces with hyphens to match the naming
conventions. The plugin can be configured to return either a list of IDs only or the full details of the integration
IDs. It has three possible outcomes: returning the found integration IDs, indicating a missing ID, or reporting an error
if the retrieval process fails.

# Inputs and Outputs

- **Inputs:** The plugin accepts input through the "payload" port, which should contain the profile data.
- **Outputs:** There are three possible outputs:
    - **payload:** Returns the integration ID(s) for the profile if found.
    - **missing:** Indicates that no integration ID was found for the profile.
    - **error:** Returns an error message if the plugin encounters an issue during execution.

This plugin does not initiate workflows but acts within them, processing and returning data based on the profile's
integration IDs.

# Configuration

- **External System Name:** The name of the external system for which the integration ID should be retrieved. The plugin
  converts this name to lowercase and replaces spaces with hyphens.
- **Get only IDs:** A boolean option. When true, the plugin returns only the IDs of the integrations. When false, it
  returns the full details of the integrations.

# JSON Configuration

```json
{
  "name": "example-system",
  "get_ids_only": true
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

This plugin works with all types of events and does not require the event to be synchronous. It is not a UIX widget, so
it does not wait for the workflow to finish before proceeding.

# Errors

- **Name can not be empty.** This error occurs if the External System Name configuration is left blank. Ensure this
  field is filled out with the name of the external system you're trying to integrate with.
- **Generic error message (e.g., "An unexpected error occurred").** If the plugin encounters an unexpected issue during
  execution, a generic error message will be returned. This could be due to network issues, database access problems, or
  other unforeseen errors.