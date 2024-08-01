# Send to MixPanel plugin

This plugin sends currently processed event to given MixPanel project.

## Requirements

This plugin requires MixPanel account, project and resource, containing project's token and server prefix. Service
account credentials are not required for this particular plugin.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns given payload on port **success** if action was successful, or on port **error** if one occurs.

## Configuration

### Form fields

- MixPanel resource - Select your MixPanel resource, containing project's token and server prefix (either EU or US)
- Additional fields mapping - Here you can add custom mapping for your event. Feel free to use dotted notation.

### Advanced configuration

```json
{
  "source": {
    "id": "<id-of-your-mixpanel-resource>",
    "name": "<name-of-your-mixpanel-resource>"
  },
  "mapping": {
    "<custom-key-1>": "<path-1>",
    "<custom-key-2>": "value-1"
  }
}
```