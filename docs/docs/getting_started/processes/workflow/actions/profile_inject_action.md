# Load profile by ...

This plugin is designed to load and replace the current profile in a Tracardi workflow. It also assigns the loaded
profile to the current event, effectively replacing the current profile with the newly loaded one.

# Version

0.8.2

## Description

The "Load profile by ..." plugin operates by identifying a profile based on a specified field and its value. This field
is a piece of personally identifiable information (PII) unique to each profile, such as an email address or phone
number. Once the field and its corresponding value are provided, the plugin searches for the profile in the database. If
found, it updates the workflow's current profile and assigns it to the current event.

The plugin handles different scenarios:

1. If the specified field is 'id', it loads the profile directly based on the provided ID.
2. For other fields, it searches for an active profile that matches the provided field and value. If exactly one
   matching profile is found, it is loaded; otherwise, an error is generated.

The plugin's primary function is to update the workflow's execution graph with the loaded profile, making it available
as part of the workflow's internal state.

# Inputs and Outputs

- **Inputs**: The plugin takes a payload object as its input. This payload is used to obtain the field value for profile
  identification.
- **Outputs**:
    - **Profile**: Outputs the loaded profile object if a profile is successfully found and loaded.
    - **Error**: Outputs an error message if the profile cannot be found or if multiple profiles match the search
      criteria.

# Configuration

- **Profile field**: The PII profile field used to identify the profile. Options include fields like main email,
  business email, private email, main phone, mobile phone, etc.
- **Value**: The specific value of the field, which can be a static value or a reference from the event or any object
  within the workflow.

# JSON Configuration

```json
{
  "field": "data.contact.email.main",
  "value": "event@properties.email"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- **"Could not find profile."**: This error occurs when no profile is found matching the provided field and value.
- **"Found [number] records for [field] = [value].**": This error is triggered when multiple profiles match the
  specified field and value, indicating an ambiguous search result.