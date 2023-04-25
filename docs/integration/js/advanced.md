# Advanced configurations

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

