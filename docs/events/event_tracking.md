# Event tracking

## Core definition

### Tracker payload

A tracker payload is an object that contains all the data associated with an event. This includes event properties, context, profile id, and session id. It is a comprehensive representation of the event that includes all the necessary data to understand the event. Tracker payload is sent to the system collector which collects data.

## Introduction - keeping track of events

Sending events is a way of tracking customer behavior in order to better understand and respond to their actions. By capturing and analyzing events, we can gain insights into how customers interact with our systems and products. This information can be used to identify trends, patterns, or opportunities for improvement, and can help us to more effectively support and assist customers, such as during the purchasing process. 

## Event example

Events consist of three main components:

1. The event type: This is a label that identifies the type of event that has occurred. For example, an event type might be "product purchase" or "login attempt".

2. Event properties: These are the characteristics or attributes of the event that describe the specifics of the event itself. For example, an event that represents a user clicking a button might have properties such as the type of button, the location of the button, and the time at which the event occurred.

3. Context: This refers to data that provides additional context or background information about the event. This data may not be directly related to the event itself, but it can provide valuable insights into the circumstances surrounding the event. For example, if an event represents a customer making a purchase at a store, the event context might include information about the weather conditions at the time of the purchase.


## Event registration

To register an event with Tracardi, you will need to send a POST request to the `/track` endpoint on the server where Tracardi is installed. 


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

This POST request to the specified URL with the event data and additional information about the source and session. If the request is successful (i.e., the server returns a status code of 200), the code will print a message indicating that the event was registered successfully. If there was an error, it will print the error message returned by the server.

Note that not all data is required. Below you can find example with only required data.

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
* `saveEvents` - True / False value - whether tracardi should save the event or just process it

### Example of debugger data

```json title="Example of debugger data"
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

## Tracking events with webhook

A webhook is a way for an application to provide other applications with real-time information. It allows one application to send a message or information to another application when a specific event or trigger occurs. 

Webhooks are typically used to send data from one application to another over the internet. They can be used to connect a wide variety of applications and services, such as social media platforms, payment gateways, and customer relationship management systems.

### Profile-less events and webhooks

In some cases, we may not have access to a customer's profile data but we do have an identifier that allows us to identify the customer. An example of this scenario might be when we have a discount coupon and we know which customer received the coupon on external systems, but we do not have access to that information at the time of the event (which only includes the voucher ID). In these situations, we can send profile data as a profile-less event. This means that the system will not have a profile ID or create a new profile.

However, it is possible to retrieve customer data from external systems and attach the appropriate profile at the time of event processing. This enables us to track and analyze customer data even when profile information is not available at the time of the event.

## How to send profile-less event

There are two ways to send profile-less events.

First, by adding the profile_less parameter to the POST / track query. In this way

```
POST /track?profile_less=true
```

A profile-less event will not create a profile, but it will create a session. The data sent to the server must include a session ID, which can be either an existing session or a new one generated on the client-side. It is important to note that a profile-less event will not have a profile when it enters the workflow. The profile field will be empty.

Another way to send a profile-less event is to post it to the endpoint:

```
POST /collect/EVENT-TYPE/SOURCE-ID
```

where:

* EVENT-TYPE is the event type, e.g. coupon-received and
* SOURCE-ID is the event source id.

In the body of the query, we send an ordinary object in the form of JSON, which will become the properties of this
event.

!!! note

    Please note that sending an event in this manner will not create a session. However, it is possible to add a profile and a 
    session during event processing. This allows for the dynamic linking of the profile to the event within the workflow.

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
