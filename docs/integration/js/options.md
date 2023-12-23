# Event options

Event options in Tracardi allow you to define the behavior of events and add contextual information associated with an
event. When events are triggered using the Tracardi JavaScript snippet, they automatically include default context
information, such as browser information and metadata, to provide additional details about the event.

## Default Event Context in JavaScript Snippet

The default event context attached by the Tracardi JavaScript snippet includes the following information:

```json
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

## Customizing Event Context

You can add additional context information to events by including a "context" key in the options when triggering events
using the Tracardi JavaScript snippet. For example:

```javascript title="Example" linenums="1" hl_lines="5"
window.tracker.track(
   "page-view",
   {},
   {
    "context": {"tag": "search"}
   });
```

In the example above, a custom context object with a "tag" key and value "search" is added to the event options. This
allows you to include additional information that is relevant to your specific use case.

## Immediate tracks

By default, tracking events are accumulated in a set of tracks and dispatched once the page loading completes. The
timing of event dispatch is crucial and depends on how the event is sent using your JavaScript code.
Typically, `window.tracker.track` is used for sending events, and it's vital to configure these events to fire
instantly, particularly if they're collected post page load. To achieve this, you should add the `fire: true`
option in your `window.tracker.track` call. This specific option commands the event to trigger immediately, without
waiting for the entire page to load or after the page has loaded. Incorporating `fire: true` ensures the event
is transmitted to Tracardi as soon as the function executes.

```javascript title="Example" linenums="1"
window.tracker.track("purchase-order", {}, {"fire": true});
```

## Beacon tracks

Beacon events in Tracardi are events that are sent even if the customer leaves the page. These events allow you to track
user interactions that may occur after a user has navigated away from a page, providing valuable insights into user
behavior.

To configure a beacon event in Tracardi, you can add the asBeacon: true option to the track configuration. This
indicates that the event should be sent as a beacon event.

### Example of Beacon Event

Here is an example of how to configure a beacon event in Tracardi:

```javascript title="Example" linenums="1"
window.tracker.track("out-link-clicked", {}, {"fire": true, asBeacon: true});
```

In the above example, the asBeacon option is set to true, indicating that the "out-link-clicked" event should be sent as
a beacon event, even if the customer leaves the page.

Beacon events can be useful in scenarios where you want to track user interactions that may occur when user leaves the
webpage, such as form submissions, redirect button clicks, or other events that may happen after the user has navigated away from
the page.

