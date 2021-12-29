# Event tracking

## Introduction - keeping track of events

Sending events is a way to track customer behavior. Thanks to events, we can react to the customer actions and help
them, e.g. in the purchasing process.

## Event example

Events consist of:

* the event name,
* event properties, and
* context.

`The name` is a simple string of characters that identifies the event. An example event may be, for example,
a `purchase of a product`, `a page scrolled to the end`, `sing-in`, etc.

`Event properties` are additional information on the event. For example, when signing-in, we can send the user's login.
When registering `purchase order` we can send product name and price.

`Context` is additional data not necessarily related to the event, e.g. type of browser used, phone screen size, weather
conditions, etc.

## Event registration

To register an event, connect to the /track endpoint on the server where Tracardi is installed.

You need to write a code that will connect to the POST method to the url e.g.
http://tracardi.page.com/track and send the data about event plus additional information on the source and session.

```json title="Example of track data payload" linenums="1" hl_lines="13-24"
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "profile": {
    "id": "profile-id"
  },
  "context": {},
  "properties": {},
  "events": [ 
    {
      "type": "purchase-order",
      "properties": {
        "product": "Nike shoes",
        "quantity": 1
      }
    },
    {
      "type": "page-view"
    }
  ],
  "options": { 
    
  }
} 
```

Not all data is required. Below you can find only required data.

```json title="Only required payload data"
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "events": [
    {
      "type": "purchase-order",
      "properties": {
        "product": "Nike shoes",
        "quantity": 1
      }
    },
    {
      "type": "page-view"
    }
  ]
} 
```

When registering an event, we need the following data.

* Data about the event, i.e. `the type of the event` and its `properties`. There may be several events within one query.

* `Source id`. It must match the event source ([inbound traffic](../getting_started/core_definitions.md#traffic)) defined in Tracardi.
  Otherwise the Authorization error wil be returned.

* And the `session id`. The session id is the saved id of the last session. If this is the first visit, you should
  generate id, preferably using uuid4 and attach it to the payload. Visits are related with the session, so the session
  id should change with each new user visit. Read more on session in
  the [core definitions section](../getting_started/core_definitions.md#session)

Additionally, the `profile id` should be sent to the system. For the first visit, there is no profile id so profile id
field is not sent. After first connection Tracardi will return a profile id that should be attached with each subsequent
connection to /track endpoint.

If no `profile id` is defined in sent data then new profile id will be generated.

If you want to send `context` attach it to context field. Context as well as properties may have any schema.

Example of event data payload with context `attached`.

```json
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "profile": {
    "id": "profile-id"
  },
  "events": [
    {
      "type": "purchase-order",
      "properties": {
        "product": "Nike shoes",
        "quantity": 1
      }
    },
    {
      "type": "page-view"
    }
  ],
  "context": {
    "device": "iPhone X"
  }
} 
```

## Event options

There is an `options` section in the data sent to tracardi. It allows you to configure how the server should respond to
the query.

```json title="Example of track data payload with options" linenums="1" hl_lines="20"
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "events": [
    {
      "type": "purchase-order",
      "properties": {
        "product": "Nike shoes",
        "quantity": 1
      }
    },
    {
      "type": "page-view"
    }
  ],
  "options": {}
} 
```

We have the following options.

* `debugger` - True / False value - whether Tracardi should send back data on how the workflow has gone through, if the
  events and profiles have been created. E.g. In a production environment, the debugger should be set to False.
* `profile` - True / False value - whether tracardi should send back the full user profile or just his id. In most
  cases, the id alone is enough.
* `saveSession` - True / False value - whether tracardi should save the session data.
* `saveEvent` - True / False value - whether tracardi should save the event or just process it

### Example od debugger data

```json title="Example od debugger data"
{
  "debugging": {
    "session": {
      "saved": 1,
      "errors": [],
      "ids": [
        "string"
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
    },
    "execution": {},
    "segmentation": {
      "errors": [],
      "ids": []
    },
    "logs": []
  }
}
```

## Profile less events

There are cases where we do not have profile data, but we do have an ID that will allow us to identify the customer as
part of the event. An example would be a discount coupon. We have identified who received which voucher on external
systems, but we are not able to obtain this information at the time of purchase. Therefore, we can send Tracardi **less
profile** requests. It will not have a profile ID, and it will not be created either. Remember that, in principle, for
each event, if we don't send an id profile, it will be created and returned for the client (program) to store and send
it on each subsequent event.

There are two ways to send profile less events.

First, by adding the profile_less parameter to the POST / track query. In this way

```
POST /track?profile_less=true
```

Such an event will not create a profile, but will create a session. There must be a session id in the data sent to the
server. It can be an existing session or a new one generated on the client-side. Remember that a profile_less event will
not have a profile when it goes to workflow. The profile will be empty.

Another way to send a less event profile is to post it to the endpoint:

```
POST /collect/EVENT-TYPE/SOURCE-ID
```

where:

* EVENT-TYPE is the event type, e.g. coupon-received and
* SOURCE-ID is the event source id.

In the body of the query, we send an ordinary object in the form of JSON, which will become the properties of this
event.

!!! note

    The event sent in this way will not create a session. Of course, it is possible to add a 
    profile and a session while processing the event. In this way, we could connect the profile 
    to the event dynamically in the workflow.

# Response

```json title="Example of the response without debugging information"
{
  "profile": {
    "id": "0d2d9dc5-0d60-471e-956f-8766dcb8aba2"
  },
  "source": {
    "consent": false
  }
}
```
