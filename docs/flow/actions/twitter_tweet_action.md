# Twitter tweet publisher

This plugin adds tweets on your twitter feed.

## Requirements

You'll need a twitter account where you need to create a application and generate access keys. There are 4 keys in
total. For more details check twitter resource documentation.

## Input

This plugin takes any payload.

## Output

Depending on the response the plugin it will trigger result port (if the response was successful) or error if the response
has an error.

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