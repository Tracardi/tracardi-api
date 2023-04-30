This documentation provides information on how to use the Tracardi platform to send events in real-time. It explains how
to set the `fire` parameter to `true` when making API requests or using the Tracardi JavaScript snippet on a web page in
order to bypass the event queue and send the events without any delay. This feature is particularly useful in scenarios
where real-time data processing is critical, such as tracking user interactions, capturing user behavior, and
implementing dynamic marketing strategies.

The documentation also provides an example of how to break the event queue and trigger an event immediately upon a
certain event type by setting the `fire` parameter to `true` in the JavaScript code. Additionally, it explains how to
bind events directly to page elements, such as buttons, using JavaScript code. In this case, the event is recorded in
the console but not sent to Tracardi by default. To trigger the event and send it to Tracardi immediately, the `fire`
attribute with a value of `true` must be added as a parameter to the window.tracker.track function.