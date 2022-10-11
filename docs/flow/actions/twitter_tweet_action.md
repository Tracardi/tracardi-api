# Twitter tweet publisher

This plugin add tweets on your twitter.

## Requirements

You'll need a twitter account from which you'll create application to generate access keys, there are 4 keys in total. For more details check twitter resource documentation.

## Input

This plugin takes any payload.

## Output

Depending on the response result it will trigger other payload port (if the response is successful) or error for if the response indicates that tweet wasn't send.


## Config

Plugin's configuration requires information about API key, sender email, 
message recipient's email(s), message subject and message content.

```json
{
  "source": {
    "id": "<id-of-your-twitter-resource>",
    "name": "<name-of-your-twitter-resource>"
  },
  "tweet": "Tweet content"
}
```