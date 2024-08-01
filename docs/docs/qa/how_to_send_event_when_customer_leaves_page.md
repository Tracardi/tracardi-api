# How can I send the event of a customer leaving the page?

To detect and handle the event of a customer leaving a webpage in Tracardi, you can use JavaScript to listen for events
that typically signify a user's intent to exit. These events include beforeunload and unload. Here’s a general approach
on how to capture these events and send them to Tracardi:

First, add an event listener to the window object for beforeunload or unload. The beforeunload event can ask the user
for confirmation before leaving the page and can be used to trigger a send to Tracardi.

Here's an example of how you might write the JavaScript to capture these events:

```javascript
window.addEventListener("beforeunload", function(event) {
    // Optionally, you can prompt the user to confirm the page exit
    event.preventDefault(); // Chrome requires returnValue to be set
    event.returnValue = '';

    // Data you might want to send to Tracardi
    const eventData = {
            "timestamp": new Date().toISOString(),
            "message": "User is leaving the page"
        };

    // Track event with Tracardi
    window.tracker.track("page-exit", eventData, {fire: true});
});
```

Other way is to use the beacon event on the click of the external link.

Example

```html
<a href="http://external-page.com" onClick="window.tracker.track('page-exit', {}, {fire: true, asBeacon: true});
```

More on beacon events can be found [here](how_to_send_event_on_a_click_that_goes_to_external_page.md)

