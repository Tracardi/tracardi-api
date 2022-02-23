# Assign condition results plugin

This plugin resolves a set of conditions and set profile fields.

## Input

This plugin takes any payload as input.

## Output

This plugin returns given payload on port **payload** without any changes.

## Plugin configuration

#### Form fields

- Conditions - key-value pairs, where key is a path to field in profile, and value is a condition to be resolved. 
  (e.g. profile@consents.marketing-consent: profile@consents.marketing EXISTS). Every key must start with 'profile@'.

#### JSON configuration

Example

```json
{
  "conditions": {
   "profile@consents.marketing-consent": "profile@consents.marketing EXISTS",
   "profile@interests.computers": "session@context.browser.url == \"http://computers.com\""
  }
}
```