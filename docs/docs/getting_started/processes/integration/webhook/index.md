# Webhook Integration

## Overview

Tracardi supports integration via webhooks, which are endpoints that allow external systems to send data to Tracardi
without requiring a predefined data schema. This flexibility makes webhooks an excellent choice for integrating various
external services with Tracardi.

## Webhook URL

Event properties should be sent in the body of the request or as URL parameters. The event-type inside the URL should be
replaced with the event type you would like to emit.

Example Webhook URL:

```bash title="Example webhook call"
/collect/<event_type>/<source_id>
```

## Webhook URL with Session

If you can add a session ID to your URL, the user profile will be recreated. Use this webhook if you have access to the
Tracardi user session. Replace session_id with the user session ID and type your event type instead of event-type. Event
properties should be sent in the body of the request or as URL parameters.

Example Webhook URL with Session:

```bash title="Example webhook call with session"
/collect/<event_type>/<source_id>/<session_id>
``` 

Here are the parameters described:

- **/collect**: This is the base endpoint indicating that the URL is intended for data collection via a webhook in
  Tracardi.

- **<event_type>**: This placeholder should be replaced with the specific type of event you are collecting. The event
  type is a string that describes the nature of the event, such as "page-view", "purchase", "click", etc.

- **<source_id>**: This is the Source ID, a unique identifier for the source of the event. It tells Tracardi which
  source configuration to use when processing the incoming data.

- **<session_id>**: Replace this placeholder with the unique session ID associated with the current user session. The
  session ID is utilized to retrieve the corresponding user profile. If the session is recognized within the system, the
  profile that initiated it will be linked to the webhook event.

## Available Webhooks

Below are the available webhooks in Tracardi:

- **POST /collect/EVENT-TYPE/SOURCE-ID**: Collects data from a POST request with an event type and source ID. It can create profile-less events with the provided properties.
- **GET /collect/EVENT-TYPE/SOURCE-ID**: Similar to the POST method, this endpoint collects data from a GET request with an event type and source ID. It can also create profile-less events based on query parameters.
    
- **POST /collect/EVENT-TYPE/SOURCE-ID/SESSION-ID**: Collects data from a POST request with an event type and source ID and session ID.
- **GET /collect/EVENT-TYPE/SOURCE-ID/SESSION-ID**: Similar to the POST method, this endpoint collects data from a GET request with an event type and source ID and session ID.

