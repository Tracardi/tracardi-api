# Has consents

This plugin checks if certain consents are granted by the current profile in a workflow. It is particularly useful for
workflows that involve conditional processing based on user consents.

# Version

0.6.2

## Description

The 'Has consents' plugin operates by evaluating a set of specified consent IDs against the consents granted to a
profile. It allows you to define a list of consent IDs and check whether these consents are granted and not revoked. The
plugin can be configured to require all specified consents to be granted or to accept the granting of any one of the
specified consents.

Here's a step-by-step explanation of how the plugin works:

1. The plugin first checks if the event is profile-less. If it is, the plugin cannot perform a consent check and will
   return the payload on the 'false' port.
2. It then processes each consent ID specified in the configuration. For each ID:
    - If the consent type does not exist, it raises an error.
    - If the 'Require all' setting is enabled, it checks if all consents are granted; otherwise, it checks if at least
      one consent is granted.
    - For revokable consents, it also checks if the consent has not been revoked.

If all conditions are met, the payload is returned on the 'true' port; otherwise, it is returned on the 'false' port.

# Inputs and Outputs

Inputs:

- **payload**: Accepts any payload object.

Outputs:

- **true**: Returns the payload if the defined consents are granted.
- **false**: Returns the payload if the defined consents are not granted.

# Configuration

- **IDs of required consents**: List of consent IDs that the profile must grant. Multiple consents can be added.
- **Require all**: Determines if all specified consents must be granted (ON) or if only one granted consent is
  sufficient (OFF).

# JSON Configuration

Example configuration in JSON format:

```json
{
  "consent_ids": [
    {
      "id": "consent1"
    },
    {
      "id": "consent2"
    }
  ],
  "require_all": true
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- **"There is no consent type with ID [ID]"**: Occurs if a specified consent ID does not exist in the system.
- **"Corrupted data - no revoke date provided for revokable consent type [ID]"**: Occurs if revoke data for a revokable
  consent type is missing or corrupt.
- **"Cannot perform consent check on profile less event."**: Occurs if the event associated with the plugin execution
  does not have an associated profile.

The plugin is especially valuable in scenarios where consent management is crucial, ensuring that only profiles with the
necessary consents can proceed through specific parts of a workflow.