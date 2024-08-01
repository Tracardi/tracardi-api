# API integration

Integrating Tracardi with a web page or other systems is easy by calling the Tracardi endpoint.

## Track Endpoint

Events can be sent via the `/track` endpoint using the POST method and sending Tracker Payload

## Tracker Payload

There are two parts of this Tracker Payload:

* **Track Payload**: Consists of metadata such as `source.id`, `profile.id`, `session.id`, `options`, and `context`
* **Event Payload**: That consists events. This is the data inside the `events` key. It consists of
  event `type`, `properties`, etc.

```json title="Example of Tracker Payload, Highlighed Event Payload" linenums="1" hl_lines="15-29"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID"
  },
  "context": {
    // Context data
  },
  "properties": {},
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      },
      "options": {
        // Event options
      },
      "context": {
        // Additional context data
      }
    },
    ...
  ],
  "options": {}
}
```

The payload has the following data:

| Attribute  | Type           | Description                                          |
|------------|----------------|------------------------------------------------------|
| events     | List of Event  | List of events                                       |
| source     | dict           | Source object (required)                             |
| session    | dict           | Session object (required)                            |
| profile    | dict           | Profile object (required)                            |
| properties | Optional[dict] | Properties associated with the event (may be empty)  |
| options    | Optional[dict] | Additional options for the event (may be empty)      |
| context    | Optional[dict] | Additional context data for the event (may be empty) |
| tags       | Optional[list] | Tags associated with the event (optional)            |

Tracardi can collect several events in one request for one profile. That's why we define a list of objects in the events
key. Each event may have different context and can also inherit values from the tracker payload. Here's an example of the tracker
payload that could be sent to Tracardi.

```json title="Full-fledged tracker payload with a lot of data" hl_lines="11-48"
{
  "source": {
    "id": "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
  },
  "session": {
    "id": "bfb3-bf0c8c8d3387-3ee63fc6-490a-4fd8"
  },
  "profile": {
    "id": "bf0c8c8d3387-3ee63fc6-490a-4fd8bfb3"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "My Page"
      },
      "options": {
        "saveEvent": false,
        "saveSession": false,
        "debugger": false
      },
      "context": {
        "tag": "product-details-page"
      }
    },
    {
      "type": "consent-granted",
      "properties": {
        "marketing": false,
        "general": true
      },
      "options": {
        "profile": true,
        "saveSession": false
      }
    },
    {
      "type": "product-in-basket",
      "properties": {
        "product": "Adidas sneakers",
        "price": 34.43
      },
      "options": {
        "profile": false,
        "logs": false
      }
    }
  ]
}
```

!!! Notice

    Not all the fields are required.

    The required fields are: `source.id`, `session.id`, `profile.id` if exists, and collection of `events`

```json title="Minimalistic tracker payload could look like this"
{
  "source": {
    "id": "f14dc4b1-8dd8-4fc1-bd14-d6823ba7013e"
  },
  "session": {
    "id": "d6823ba7013e-8dd8-4fc1-bd14-f14dc4b1"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "My Page"
      }
    },
    {
      "type": "product-in-basket",
      "properties": {
        "product": "Adidas sneakers",
        "price": 34.43
      }
    }
  ]
}
```

### Custom times

There can be a need to send historical sessions and profile to Tracardi with the old timestamps. This can be done by
setting the profile and session metadata.

#### Session Default Times

To override the session timestamps, you can use the session object. Add additional metadata to define the default values
that will be used when the session is created. This is particularly useful if you are importing old data or want to pass
the `create` time from your client. `Metadata` is optional.

!!! Note

      This feature is available from version 0.9.0.

```json title="Example of track data payload with session times" linenums="1" hl_lines="7-11"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID",
    "metadata": {
      "create": "2023-01-01 00:00:00",
      "insert": "2023-01-01 00:00:01",
      "update": "2024-01-01 00:00:01"
    }
  },
  "profile": {
    "id": "Profile ID"
  },
  "properties": {},
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      }
    },
    ...
  ]
}
```

#### Profile Default Times

To override the profile timestamps, you can use the profile object. Add additional metadata to define the default values
that will be used when the profile is created. This is particularly useful if you are importing old data or want to pass
the `create` time from your client. `Metadata` is optional.

!!! Note

      This feature is available from version 0.9.0.

```json title="Example of track data payload with profile times" linenums="1" hl_lines="10-14"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID",
    "metadata": {
      "create": "2023-01-01 00:00:00",
      "insert": "2023-01-01 00:00:01",
      "update": "2024-01-01 00:00:01"
    }
  },
  "properties": {},
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      }
    },
    ...
  ]
}
```

### Profile IDs

Additional profile IDS can be appended to the profile during event consumption. To do so, add `IDs` as an array of
strings to the profile object. `Ids` are optional.

!!! Note

      This feature is available from version 0.9.0.

```json title="Example of track data payload with profile ids" linenums="1" hl_lines="10-14"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID",
    "ids": [
      "id1",
      "id2",
      "id3"
    ],
    "metadata": {
      "create": "2023-01-01 00:00:00",
      "insert": "2023-01-01 00:00:01",
      "update": "2024-01-01 00:00:01"
    }
  },
  "properties": {},
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      }
    },
    ...
  ]
}
```

### Context

Context encompasses supplementary information or data that offers a wider perspective on an event. It includes
pertinent details that contribute to a deeper comprehension of the event's surrounding circumstances. There are two
types of context, Track Context and Event Context. Track context is defined on the level of Tacker Payload. Event
Context is
defined inside the event object.

```json title="Tracker Context that will be saved in Session" linenums="1" hl_lines="16-33"
{
  "source": {
    "id": "f14dc4b1-8dd8-4fc1-bd14-d6823ba7013e"
  },
  "session": {
    "id": "d6823ba7013e-8dd8-4fc1-bd14-f14dc4b1"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "My Page"
      }
    }
  ],
  "context": {
    "browser": {
      "local": {
        "browser": {
          "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
      }
    },
    "location": {
      "country": {
        "code": "PL",
        "name": "Poland"
      },
      "city": "Warsaw",
      "longitude": 15.634,
      "latitude": 48.1962,
      "zip": "3100"
    }
  }
}
```

```json title="Event Context that will be saved in Event" linenums="1" hl_lines="14-16"
{
  "source": {
    "id": "f14dc4b1-8dd8-4fc1-bd14-d6823ba7013e"
  },
  "session": {
    "id": "d6823ba7013e-8dd8-4fc1-bd14-f14dc4b1"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "My Page"
      },
      "context": {
        "page": "http://tracardi.com"
      }
    }
  ]
}
```

### Options

Event options provide additional instructions or directives related to the processing of an event. They can specify how
the event should be handled, what actions to take, or what data to return as a result of processing the event. Here are
some examples of what can be included as event options:

```json title="Options" linenums="1" hl_lines="16-20"
{
  "source": {
    "id": "f14dc4b1-8dd8-4fc1-bd14-d6823ba7013e"
  },
  "session": {
    "id": "d6823ba7013e-8dd8-4fc1-bd14-f14dc4b1"
  },
  "events": [
    {
      "type": "page-view",
      "properties": {
        "pageTitle": "My Page"
      }
    }
  ],
  "options": {
    "saveEvent": false,
    "saveSession": false,
    "debugger": false
  }
}
```

Here is the description of the configuration options in a table format:

| Option      | Description                                                                                                                                                |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| saveEvent   | Determines whether the event should be saved or treated as ephemeral. If set to `false`, the event is processed but not permanently saved.                 |
| saveSession | Specifies whether the session associated with the event should be saved. If set to `false`, the session data will not be stored for this particular event. |
| debugger    | Controls the inclusion of debugger information in the event response. If set to `false`, debugger information will not be returned.                        |

## Tracker Payload, Event Payload

Event payload is the part of Track Payload that has events data:

```json title="Highlighed Event Payload" linenums="1" hl_lines="14-28"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID"
  },
  "context": {
    // Context data
  },
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      },
      "options": {
        // Event options
      },
      "context": {
        // Additional context data
      }
    },
    ...
  ]
}
```

### Event type

An event type refers to the specific kind of interaction or activity that is tracked and recorded within the system. It
categorizes events based on their nature, such as page views, clicks, form submissions, purchases, or custom-defined
actions.

Define event type as slug of its name. For example if the event type is `Page View` set `type` to `page-view`.

### Events Default Times

To send an event, you can populate the attributes described above according to your specific event data. If you wish to
override the current insert time, which represents the time of event collection, and instead use a custom time, you can
set the `time.insert` attribute to the desired date and time.

The same principle applies to the `create` and `update` attributes. If you want to provide custom timestamps for event
creation or update, you can set the corresponding values of `time.create` and `time.update` to the appropriate dates and
times.

By customizing the `time` attributes, you can have more control over the temporal aspects associated with the event,
ensuring accurate representation within your event tracking system.

```json title="Example of track data payload with event times" linenums="1" hl_lines="17-21"
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID"
  },
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      },
      "time": {
        "create": "2023-01-01 00:00:00",
        "insert": "2023-01-01 00:00:01",
        "update": "2024-01-01 00:00:01"
      }
    },
    ...
  ]
}
```

### Properties

Event properties refer to specific attributes or characteristics that provide relevant details about an event. They
contain the actual data associated with the event and can vary depending on the nature of the event and the specific
requirements of the system or application. Here are some examples of what can be included as event properties:

1. User information: Information about the user involved in the event, such as user ID, username, email address, or any
   other relevant user identifiers.
2. Event parameters: Parameters or values that capture specific aspects of the event, such as quantity, price, duration,
   location, or any other measurable or meaningful attributes.
3. Status indicators: Flags or indicators that reflect the status or outcome of the event, such as success, failure,
   pending, or in-progress.
4. Metadata: Additional contextual information or metadata that provides further insights into the event, such as event
   source, event category, or any custom-defined metadata specific to the application or system.

Event properties serve to enrich the event data, allowing for a more detailed and meaningful representation of the event
within the system or application.


## Tracker response

This is the example of the response from Tracardi after the events were collected.

```json
{
 "task": [
  "fae054ab-fab4-4eaf-8762-f8b71638b043"
 ],
 "ux": [],
 "response": {},
 "events": [],
 "profile": {
  "id": "60a05b82-0554-48a6-a53c-b759031a8f0b"
 },
 "session": {
  "id": "4812b132-1c07-4b68-899b-d18b5c24b6e6"
 },
 "errors": [],
 "warnings": []
}
```

### Response Schema Description


| Key       | Description                                                              | Example Value                                                                 |
|-----------|--------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| task      | List containing the Task ID                                              | ["fae054ab-fab4-4eaf-8762-f8b71638b043"]                                      |
| ux        | List of JavaScript widgets to include on the page                        | [{"tag":"script","type":"text/javascript","content":["\n  (function(d,t) "]}] |
| response  | Response data from workflow (requires synchronous event)                 | {"data": "value"}                                                             |
| events    | List of events                                                           | []                                                                            |
| profile   | Profile information                                                      | {"id": "60a05b82-0554-48a6-a53c-b759031a8f0b"}                                |
| session   | Session information                                                      | {"id": "4812b132-1c07-4b68-899b-d18b5c24b6e6"}                                |
| errors    | List of errors                                                           | ["error message"]                                                             |
| warnings  | List of warnings                                                         | ["warning message"]                                                           |

Response key can be considered as the output of workflows, which are executed based on the configurations and logic
defined within them. These responses from multiple workflows are consolidated into a single response, which can then be further
processed, analyzed, or used to trigger subsequent actions.

Responses may also contain additional information, such as the response key, which is a defined field that includes the
data returned by a specific workflow. The response key helps organize and structure the data collected from different
workflows, making it easier to access and utilize in downstream processes.


## Other information

### Obtaining the Profile ID

To obtain the profile ID, the recommended approach is to send the tracker payload without setting the profile ID, and
only generate the session ID. Tracardi will then return the generated profile ID, which needs to be saved on the client
side. This is how the Tracardi JavaScript snippet works, by saving the profile ID in the browser's localStorage and the
session ID in cookies. Please refer to [Tracking](../../../processes/tracking.md) to understand how tracking works.

### Changing Session ID while Keeping Profile

In some cases, the client may want to keep the profile unchanged but change the session ID. To achieve this, the client
can provide the profile ID while generating a new session ID. This will result in a new session being created, while the
profile remains unchanged, and the system generates a new visit for the user.

### Sending Same Session ID with Tracking Payloads

While it is possible to send the same session ID with all the tracking payloads, allowing the system to keep the session
and profile unchanged, this practice is not suggested. This is because if a profile is saved with only one visit, it
will not be possible to change the visits associated with the profile. It is recommended to generate a new session ID
for each visit to ensure accurate tracking and profiling of user behavior.

### How to integrate Tracardi with mobile apps or external systems

Integrating Tracardi with mobile apps or external systems follows a similar process as integrating with a web page, with
the only difference being that Tracardi provides a JavaScript snippet for a web page that simplifies the integration. The JavaScript
snippet automates the process of calling the track endpoint and saving the Session ID and Profile ID in the browser.

However, when integrating with mobile apps or backend systems, the process needs to be done manually. It is crucial to
remember that both the Profile ID and Session ID must be saved on the customer's device or backend system for effective
[tracking](../../../processes/tracking.md).

While it may be evident to save the Profile ID and Session ID when integrating with a mobile app, it may not be as
apparent when integrating with a PHP application or other server-side applications. In such cases, it is necessary to
set a PHPSESSIONID or other relevant token that can be used to track the customer and store the Tracardi Profile ID and
Session ID within the defined user session. This ensures that the data collected by Tracardi can be accurately
associated with the correct customer profile and used for further personalization or analysis.

It is essential to follow these steps diligently when integrating Tracardi with mobile apps or external systems to
ensure error-free [tracking](../../../processes/tracking.md).

# Errors

## Response - 422 Unprocessed entity

This error occurs when the tracker payload is missing some data. Usually it will happen when you miss required field.

## Response - Unauthorized

This error occurs when the `source.id` that is sent with payload does not exist in Tracardi.

## Response - Headers

With response there is a `x-process-time` header thar returns how much time it took to process the request.