# Send Twitter tweet plugin 

This plugin adds tweets on your Twitter feed.

## Requirements

You'll need a Twitter account where you need to create an application and generate access keys. There are 4 keys in
total. For more details check twitter resource documentation.

## Input

This plugin takes any payload.

## Output

Depending on the response, the plugin will trigger data on __response__ port (if the response was successful) or on 
__error__ port if the response had an error.

## Config example

```json
{
  "source": {
    "id": "<id-of-your-twitter-resource>",
    "name": "<name-of-your-twitter-resource>"
  },
  "tweet": "Tweet content"
}
```

Tweet can be a message template. Template is a text file with special mark-up. Within double curly braces you can place
dot notation that reads data from internal state of the workflow.

__Example__

```
Hello {{profile@pii.name}}
```
