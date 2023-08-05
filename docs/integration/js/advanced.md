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

## Forcing Profile ID

In certain situations, you may want to send a specific profile ID to Tracardi that comes from your backend system. To
enable this feature, static ID must be enabled in the event source that collects data, and the profile ID must be added
to the script configuration.

Here's an example:

```html title="Example" linenums="1" hl_lines="15-17"

<script>

        !function(e){"object"==typeof exports&&"undefine...  

        const options = {
            tracker: {
                url: {
                    script: 'http://192.168.1.103:8686/tracker', 
                    api: 'http://192.168.1.103:8686'
                },
                source: {
                    id: "<your-event-source-id-HERE>" 
                },
                profile: {
                    id: "<your-static-profile-id-HERE>" 
                }
            }
        }
</script>
```

It's important to note that this will send the provided profile ID regardless of whether a profile ID is already stored
in the browser's local storage. If event source si not configured to allow static profile ID then System will try
to load profile with provided ID - it will most probably fail and then it will generate the random ID. Please do
not use this feature with events sources that has disabled static profile processing in events source. 

!!! Warning

    Please be aware that sending a profile ID that's easy to guess can be a security risk. Attackers can potentially guess
    the ID and try to corrupt its data. Always use IDs like UUID4 to ensure security.

!!! Notice

    This feature is available from version 0.8.1 up.

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

