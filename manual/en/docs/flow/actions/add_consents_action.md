# Add consent plugin

This plugin appends given consents to profile.

## Configuration

The only thing taken by plugin in configuration is path to consents, so, for example *payload@info.givenConsents*.

## Consents payload

Consents payload (field that we give path to in config) should be in form of:

```json
{
    "example-revokable-consent-id": {
        "revoke": "<date-of-revoke>"
    },
    "example-irrevocable-consent-id": {
        "revoke": null
    }
}
```

Plugin takes these consents and adds them to profile if they are valid.

## Output

Plugin returns given payload (without any changes) on port *payload*.