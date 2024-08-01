# How to collect event on the external click

To send an event on a click that goes to an external page, you need to add an onClick event to the button, create a
function that will send an event when the button is clicked, and add the `fire` attribute with a value of `true` as a
parameter to the window.tracker.track function. Moreover, you also need to set beacon to True. A beacon is an event that
is sent even if the customer leaves the page. It allows you to track user interactions that may occur after a user has
navigated away from a page, providing valuable insights into user behavior.

```javascript title="Example" linenums="1"
window.tracker.track("page-view", {}, {"fire": true, asBeacon: true});
```