# 'm using my own code to send an event with window.tracker.track, but it's not showing up in Tracardi. What should I do?

To ensure your event is recognized in Tracardi when using `window.tracker.track` after the page has loaded, you need to
add `fire: true` to your call. Your code should look like this:

```javascript
window.tracker.track('event-type', properties, {fire: true});
```