# Load profile by ...

Loads and replaces current profile in the workflow. It also assigns loaded profile to current event.

In order to use this plugin you will have to __select the field that will be used to identify the profile__. There is a
limited number of fields that are unique in the profiles. In most cases it will be an __e-mail__.

Also, __a field value__ is required to load the profile. It may be a static value or it can be referenced from event or
any object inside workflow.

The default values configure the plugin to use event property __email__ and profile __data.contact.email.main__ to match the profile.

If you pass the e-mail or any value that identifies the profile in other location please select the correct path.

## Advanced JSON configuration

Example

```json
{
  "field": "data.contact.email.main",
  "value": "event@properties.email"
}
```

* Field is a field name
* Value is a value of that field

## Output

If the profile is found it will be replaced inside workflow and the current event will have the profile replaced with
the loaded one. On success the profile port is triggered with the loaded profile object.

On failure the error port is triggered with the error message. 