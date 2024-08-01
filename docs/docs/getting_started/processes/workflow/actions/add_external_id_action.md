# Save Integration Id

This plugin is designed to establish a connection between Tracardi profiles and external systems by saving an external
ID to the profile. It's useful for linking profiles with their counterparts in other systems, enhancing data integration
and synchronization.

# Version

0.8.2

## Description

The plugin works by taking an external ID and, optionally, additional data related to the external system, then saving
this information to the entity related to profile in Tracardi. The process involves converting the specified system name to a lowercase
string with hyphens replacing spaces, ensuring consistency in naming conventions. The additional data can include any
information relevant to the external system, and it can be referenced from any part of the event or payload using
Tracardi's dot notation system. The plugin has two possible outcomes: successfully saving the integration ID to the
profile or returning an error if the process fails.

# Inputs and Outputs

- **Inputs:** The plugin accepts input through the "payload" port. It expects data that includes the external ID and,
  optionally, additional related data.
- **Outputs:** There are two possible outputs:
    - **payload:** The original payload is returned, indicating successful execution.
    - **error:** An error message is returned if the plugin encounters an issue during execution.

This plugin does not initiate workflows but acts within them, processing and returning data based on the provided
inputs.

# Configuration

- **External ID:** A dot notation path referencing the external ID within the event or payload.
- **External System Name:** The name of the external system. This name will be formatted to lowercase with spaces
  replaced by hyphens.
- **Additional Data:** A JSON object containing additional data related to the external system. This data can be
  referenced from any part of the event or payload using dot notation.

# JSON Configuration

```json
{
  "id": "event@properties.id",
  "name": "example-system",
  "data": "{\"key\": \"event@properties.value\"}"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Event prerequisites

This plugin works with all types of events and does not require the event to be synchronous. It is not a UIX widget, so
it does not wait for the workflow to finish before proceeding.

# Errors

- **Id can not be empty.** Occurs if the External ID field in the configuration is left empty. Ensure this field is
  populated with the correct dot notation path to the external ID.
- **Name can not be empty.** Happens when the External System Name configuration field is left blank. Fill in this field
  with the name of the external system.
- **Generic error message (e.g., "An unexpected error occurred").** If the plugin encounters an unexpected issue during
  execution, a generic error message will be returned. This could be due to problems with data formatting, network
  issues, or other unforeseen errors.