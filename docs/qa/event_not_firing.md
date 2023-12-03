# A have sent event form javascript using window.tracker.track but I do not see it in Tracardi. This is the code:

```javascript
window.tracker.track("purchase-order", {
  "product": "Sun glasses - Badoo " + index,
  "price": 13.45
}, {
  async: false
});
```

The issue seems to be that the event "purchase-order" is not being sent from the widget to Tracardi. This could be due
to the fact that the event are waiting for the page to load before firing. To send event on demand additional option
must be added. To resolve this issue, you can add the `fire: true` option to the `window.tracker.track` call. This will instruct the event to fire
immediately, regardless of whether the page has loaded or not.

Here's the corrected code:

```javascript
window.tracker.track("purchase-order", {
  "product": "Sun glasses - Badoo " + index,
  "price": 13.45
}, {
  async: false,
  fire: true
});
```

This should ensure that the "purchase-order" event is sent to Tracardi immediately when the purchase button is clicked.