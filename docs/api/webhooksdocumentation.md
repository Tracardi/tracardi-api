Sending Profile-Less Events

To send a profile-less event, you can use two methods:

Method 1: Using the `profile_less` Parameter

You can send a profile-less event by including the `profile_less=true` parameter in the `POST /track` query:

=> POST /track?profile_less=true

A profile-less event will not create a profile but will generate a session. The data sent to the server must include a session ID, which can be an existing session or a new one generated on the client-side. It's important to note that a profile-less event will not have a profile when it enters the workflow, and the profile field will be empty.

Method 2: Direct `Endpoint Posting`

Another way to send a profile-less event is by posting it directly to the following endpoint:

=> POST /collect/EVENT-TYPE/SOURCE-ID

Where:
- EVENT-TYPE is the event type (e.g., coupon-received).
- SOURCE-ID is the event source ID.

In the body of the query, send a standard JSON object, which becomes the event's properties. This method does not create a session by default, but you can add a profile and session during event processing for dynamic linkage within the workflow.

Available Webhooks :

Below are the available webhooks in this system:

1. POST `/track`: This endpoint is used for tracking events using a POST request. It can handle both profiled and profile-less events.

2. PUT `/track`: Similar to the POST method, this endpoint allows tracking events using a PUT request.

3. POST `/collect/EVENT-TYPE/SOURCE-ID`: This endpoint is used to collect data from a POST request with an event type and source ID. It can create profile-less events with the provided properties.

4. GET `/collect/EVENT-TYPE/SOURCE-ID`: Similar to the POST method, this endpoint collects data from a GET request with an event type and source ID. It can also create profile-less events based on query parameters.

5. GET `/collect/EVENT-TYPE/SOURCE-ID`: This endpoint is used for collecting data from a GET request with an event type and source ID, potentially creating profile-less events.

6. POST `/collect/EVENT-TYPE/SOURCE-ID`: Similar to the GET method, this endpoint collects data from a POST request with an event type and source ID. It can create profile-less events based on the request's body.

7. PUT `/redirect/REDIRECT-ID/SESSION-ID`: This endpoint handles various HTTP requests for redirecting events to specific URLs based on configuration. It supports PUT, DELETE, GET, and POST methods.

Response Examples:

Here are response examples for each of the webhooks mentioned:

=> POST `/track`

Response Example:

{
  "profile": {
    "id": "0d2d9dc5-0d60-471e-956f-8766dcb8aba2"
  },
  "source": {
    "consent": false
  }
}

=> PUT `/track`

Response Example:

{
  "profile": {
    "id": "1a3b4c5d-6e7f-8g9h-0i1j"
  },
  "source": {
    "consent": true
  }
}

=> POST `/collect/EVENT-TYPE/SOURCE-ID`

Response Example:

{
  "profile": {},
  "source": {
    "consent": true
  }
}

=> GET `/collect/EVENT-TYPE/SOURCE-ID`

Response Example:

{
  "profile": {},
  "source": {
    "consent": false
  }
}

=> GET `/collect/EVENT-TYPE/SOURCE-ID`

Response Example:

{
  "profile": {},
  "source": {
    "consent": true
  }
}

=> POST `/collect/EVENT-TYPE/SOURCE-ID`

Response Example:

{
  "profile": {},
  "source": {
    "consent": false
  }
}

=> PUT `/redirect/REDIRECT-ID/SESSION-ID`

Response Example:

{
  "message": "Event redirected successfully."
}

These response examples demonstrate the expected structures of responses for each webhook, providing clarity on the data and format.
