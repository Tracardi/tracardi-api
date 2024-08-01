# Event Trigger

The `window.tracker.track` function in Tracardi is a JavaScript call used to send event data from your web page to the
Tracardi server. This function is part of the Tracardi JavaScript integration snippet and allows you to track various
user interactions on your website. Here’s a detailed description of the function and its parameters:

## Syntax

```javascript
window.tracker.track(eventType, eventProperties, options);
```

### Parameters

1. **`eventType`** (string): The type of event you want to track. This is a mandatory parameter and should be a string representing the name of the event.

   **Example:** `"page-view"`, `"purchase-order"`, `"button-click"`, etc.

2. **`eventProperties`** (object): An object containing key-value pairs that represent the properties of the event. This parameter is optional but typically used to provide additional context or data about the event.

   **Example:**
   ```javascript
   {
     "product": "Sun glasses",
     "price": 13.45,
     "category": "Accessories"
   }
   ```

3. **`options`** (object): An optional object that can include additional settings or metadata for the event. This can include properties such as `profile`, `session`, or other tracking options.

   **Example:**
   ```javascript
   {
     "fire": true,
     "context": { "type": "purchase"}
   }
   ```

#### Detailed Examples

```javascript title="Tracking a simple page view event"
window.tracker.track("page-view", {
  "url": window.location.href,
  "title": document.title
});
```

In this example:
- `"page-view"` is the event type.
- The event properties include the current page URL and the document title.

```javascript title="Tracking a purchase order with additional properties"
window.tracker.track("purchase-order", {
  "product": "Sun glasses",
  "price": 13.45,
  "category": "Accessories"
});
```

In this example:
- `"purchase-order"` is the event type.
- The event properties include product details such as name, price, and category.

```javascript title="Using Options for Profile and Immediate Event Sending"
window.tracker.track("button-click", {
  "button-id": "subscribe-button",
  "button-text": "Subscribe Now"
}, {
  "fire": true
});
```

In this example:
- `"button-click"` is the event type.
- The event properties include the button ID and text.
- The `options` object includes a specific profile ID and the `fire` property set to `true`, indicating the event should be sent immediately.

# Parts of Events

## Event type

Event type is a crucial aspect of defining events in Tracardi. It refers to the name that distinguishes events from each
other. For example, a `purchase-order` event provides information about an order, while a `page-view` event signifies a
viewed page. There are different event types in Tracardi please refer to [event types](../../../components/event.md#types-of-events) for more information.

Defining an appropriate event type is essential to ensure proper categorization and processing of events within
Tracardi. It allows you to effectively organize and analyze event data based on their type.

!!! Importance of Event Type

      Event type serves as a unique identifier for events and helps differentiate them from one another. It enables you to
      effectively manage and process events, as different events may require different handling or processing logic based on
      their type.
      
      When defining an event in Tracardi, you need to specify an event type that accurately represents the nature of the
      event. For instance, if you are tracking purchase orders, you can define the event type as "purchase-order". Similarly,
      if you are tracking page views, you can define the event type as "page-view".

## Events properties

In Tracardi, each event can have additional data that provides detailed information about the event. For example,
consider the event "interest" which sends data in the format {"Electronics": ["Mobile phones", "Accessories"]}.

Tracardi collects all events with their respective data and sends them as a single request to the Tracardi tracker
endpoint. This request is made when the web page is fully loaded, ensuring that all events and their associated data are
captured accurately.

## Event options

Event options in Tracardi allow you to define the behavior of events and add contextual information associated with an
event. When events are triggered using the Tracardi JavaScript snippet, they automatically include default context
information, such as browser information and metadata, to provide additional details about the event.

### Context

To add context add `context` kay and include it in configuration part (third parameter) of the `window.tracker.track`

```javascript title="Example" linenums="1" hl_lines="5-7"
window.tracker.track(
   "page-view",
   {},
   {
    "context": {"tag": "search"}
   }
);
```

#### Default Event Context in JavaScript Snippet

Tracardi Javascript Snippet adds default event context. It includes the following information:

```json title="Example Context"
{
  "page": {
    "url": "<page-url>",
    "path": "<page-path>",
    "hash": "<page-hash>",
    "title": "<page-title>",
    "referer": {
      "host": null,
      "query": null
    },
    "history": {
      "length": 10
    }
  },
  "ip": "127.0.0.1"
}
```

The event context includes details about the current page, such as its URL, path, hash, title, referer information (host
and query), and browsing history length. It also includes the IP address of the user.

!!! Tip

    When working with Tracardi, you have the option to configure whether or not to include page data in the context of 
    each event. This configuration is done at the tracker level and can be customized according to your requirements. 
    By adjusting the tracker context configuration, you can easily control whether or not page data is sent along with 
    each event, providing you with flexibility and control over the data captured and processed.

#### Customizing Event Context

You can add additional context information to events by including a "context" key in the options when triggering events
using the Tracardi JavaScript snippet. For example:

```javascript title="Example" linenums="1" hl_lines="5-7"
window.tracker.track(
   "page-view",
   {},
   {
    "context": {"tag": "search"}
   }
);
```

In the example above, a custom context object with a "tag" key and value "search" is added to the event options. This
allows you to include additional information that is relevant to your specific use case.

### Options

#### Immediate triggering of event

By default, tracking events are accumulated in a set of tracks and dispatched once the page loading completes. The
timing of event dispatch is crucial and depends on how the event is sent using your JavaScript code.
Typically, `window.tracker.track` is used for sending events, and it's vital to configure these events to fire
instantly, particularly if they're collected post page load. To achieve this, you should add the `fire: true`
option in your `window.tracker.track` call. This specific option commands the event to trigger immediately, without
waiting for the entire page to load or after the page has loaded. Incorporating `fire: true` ensures the event
is transmitted to Tracardi as soon as the function executes.

```javascript title="Example" linenums="1" hl_lines="2"
window.tracker.track("purchase-order", {}, {
"fire": true
});
```

#### Beacon tracks

Beacon events in Tracardi are events that are sent even if the customer leaves the page. These events allow you to track
user interactions that may occur after a user has navigated away from a page, providing valuable insights into user
behavior.

To configure a beacon event in Tracardi, you can add the asBeacon: true option to the track configuration. This
indicates that the event should be sent as a beacon event.

####### Example of Beacon Event

Here is an example of how to configure a beacon event in Tracardi:

```javascript title="Example of Beacon Event" linenums="1" hl_lines="3"
window.tracker.track("out-link-clicked", {}, {
   "fire": true, 
   asBeacon: true
});
```

In the above example, the asBeacon option is set to true, indicating that the "out-link-clicked" event should be sent as
a beacon event, even if the customer leaves the page.

Beacon events can be useful in scenarios where you want to track user interactions that may occur when user leaves the
webpage, such as form submissions, redirect button clicks, or other events that may happen after the user has navigated away from
the page.

# Triggering on user actions

## Sending event on demand

Tracardi offers the flexibility to send events immediately when the fire parameter is set to true, enabling real-time
event triggering and ensuring that data is captured and processed instantly. By default, events are queued and sent when
the web page is fully rendered, which is beneficial for consolidating events and sending them as a single request.
However, there are scenarios where sending events immediately upon certain actions, such as button clicks, is necessary.
Sending Events in Real-Time

To send events in real-time, simply set the `fire` parameter to `true` when making API requests or using the Tracardi
JavaScript snippet on your web page. This will bypass the event queue and send the events without any delay.

This feature is particularly useful in scenarios where real-time data processing is critical, such as tracking user
interactions, capturing user behavior, and implementing dynamic marketing strategies. 

### Example: Breaking the Event Queue

In some cases, you may need to break the event queue and trigger an event immediately upon a certain event type. 
You can do this by setting the fire parameter to true in your JavaScript code, as shown in the example
below:

```javascript title="Example where we break the event queue" linenums="1"
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]}, {"fire": true}) //(1)
window.tracker.track("page-view",{});
```

## Binding directly to Page Elements

You can also bind events directly to page elements, such as buttons, using JavaScript code. However, please note that in
this case, you may not have access to response data, such as profile ID, etc. The example below shows how you can add an
onClick event to a button that sends an event when clicked:

```html

<button onClick="testClick()">Test click</button>
```

Where the **testClick** function sends an event.

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1});
  }
</script>
```

Please note that in this case, the event is recorded in the console but not sent to Tracardi by default. 

```
[Tracker] Event track 
Object { type: "track", event: "page-view", properties: {…}, options: {}, userId: null, anonymousId: "642aa4a6-9a48-4c08-8fd5-f0772415c824", meta: {…} }
```

To trigger the event and send it to Tracardi immediately, you can add the `fire` attribute with a value of `true` as a
parameter to the window.tracker.track function, as shown in the example below:

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1}, {"fire": true}); // (1)
  }
</script>
```

1. This event will fire immediately.

The event "interest" will be sent immediately, because of `{"fire": true}`.

