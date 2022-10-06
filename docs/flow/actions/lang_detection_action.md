# Language detection Plugin

The purpose of this plugin is detect language from given string with meaningcloud API

# Configuration

This node requires configuration. You need have an account in meaningcloud to get access to API.

*Example*

```json
{
  "source": {
    "id": "<source-id>"
  },
  "message": "Hello world!",
  "timeout": 10
}
```

* *source.id* - enter your resource id with access token, See below for resource schema.
* *message* - enter your message.
* *timeout* - response time-out.

## Resource configuration

*Example*

```json
{
  "token": "<token>"
}
```

Please register to https://www.meaningcloud.com/developer/account/subscriptions to obtain token.

Use *Api-Token* resource template in GUI to create this kind of resource.

# Input

This node does not process input payload.

# Output

This node returns json with API response at response port if API call was successful.

*Example of successful call*

```json
{
  "status": 200,
  "body": {
    "deepTime": 0.04363226890563965,
    "language_list": [
      {
        "iso-639-1": "en",
        "iso-639-2": "eng",
        "iso-639-3": "eng",
        "language": "en",
        "name": "English",
        "relevance": 100
      }
    ],
    "status": {
      "code": 0,
      "msg": "OK",
      "credits": 1,
      "remainig_credits": 19964
    },
    "time": 0.04784107208251953
  }
}
```

