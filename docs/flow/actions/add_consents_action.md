# Add consent plugin

This plugin appends consents to profile. With this plugin you will need to provide the reference to new consent data,
for example *event@properties.consents*.

## Consents payload

The most possible use-case is when customer grants consents by filling a form. This data is sent to Tracardi as an event
with properties set to granted consents. Consents payload should be in form of:

```json
{
  "example-consent-id-1": true,
  "example-consent-id-1": false
}
```

Plugin reads a data referenced with config as consents and adds them to profile if they are valid.

## Output

If there is no error plugin returns input payload (without any changes) on port *payload*.