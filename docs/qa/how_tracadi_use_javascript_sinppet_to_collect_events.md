# How Tracardi use javascript snippet to collect events?

Tracardi collects events using a JavaScript snippet that is embedded in the web page. The snippet captures user
interactions and sends them to Tracardi's server. The events are not fired in a specific sequence.

Here is a breakdown of how Tracardi collects events using the JavaScript snippet:

- The JavaScript snippet is loaded on the web page. This snippet is typically included in the HTML of the web page.

- The snippet initializes the Tracardi tracker. The tracker is responsible for capturing and sending events to
  Tracardi's server.
- 
- The tracker batches events and sends them to Tracardi's server. All event on the page a patched and send when the page
  finished loading. This helps to reduce the number of network requests and improve performance. But there are some
  drawback. When you would like to send an event dynalically if someone click sone picture, or mouse hovers then you
  need to use on demand event collection. This requires the option `fire: true` to be added to `window.tracker.track`
  function.
