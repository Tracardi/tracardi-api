# Assign condition results plugin

This plugin assigns the result from given condition to a given field in profile.

## Input
This plugin takes any payload as input.

## Output
This plugin returns given payload on port **payload** without any changes.

## Plugin configuration
#### With form
- Conditions - here provide key-value pairs, where key is a path to some field in
  profile, and value is a condition whose result will be assigned to given
  field. (e.g. profile@consents.marketing-consent: profile@consents.marketing EXISTS).
  Every key must start with 'profile@'.

#### Advanced configuration
```json
{
  "conditions": {
   "profile@consents.marketing-consent": "profile@consents.marketing EXISTS",
   "profile@interests.computers": "session@context.browser.url == \"http://comps.com.pl\""
  }
}
```