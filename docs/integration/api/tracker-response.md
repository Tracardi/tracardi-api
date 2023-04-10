# Tracker response

This is the example of the response from Tracardi after the events were collected.

```json
{
  "debugging": {
    "session": {
      "saved": 1,
      "errors": [],
      "ids": [
        "e42d9dc5-a353-471e-dd6f-8766dcb8aba2"
      ],
      "types": []
    },
    "events": {
      "saved": 0,
      "errors": [],
      "ids": [],
      "types": []
    },
    "profile": {
      "saved": 1,
      "errors": [],
      "ids": [
        "0d2d9dc5-0d60-471e-956f-8766dcb8aba2"
      ],
      "types": []
    }
  },
  "profile": {
    "id": "0d2d9dc5-0d60-471e-956f-8766dcb8aba2"
  }
}
```

## Understanding Responses in Tracardi

In Tracardi, responses play a crucial role in collecting and processing data from various ingestion pipelines and
workflows that events pass through. Responses typically include the profile ID and may also contain additional data if
configured.

Responses can be considered as the output of workflows, which are executed based on the configurations and logic defined
within them. These responses are consolidated into a single response, which can then be further processed, analyzed, or
used to trigger subsequent actions.

Responses may also contain additional information, such as the response key, which is a defined field that includes the
data returned by a specific workflow. The response key helps organize and structure the data collected from different
workflows, making it easier to access and utilize in downstream processes.
