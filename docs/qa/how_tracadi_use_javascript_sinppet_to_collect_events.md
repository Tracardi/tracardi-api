# How Tracardi use javascript snippet to collect events?

Tracardi employs a JavaScript snippet to gather events, which is embedded within the web page. This snippet captures
user interactions and subsequently transmits them to Tracardi's server. Importantly, these events are not fired in a
specific order or sequence.

Here is a breakdown of the process by which Tracardi acquires events through the JavaScript snippet:

1. The JavaScript snippet is loaded onto the web page, typically incorporated into the HTML of the page.

2. The snippet initializes the Tracardi tracker, responsible for capturing and dispatching events to Tracardi's server.

3. The tracker aggregates events and transmits them to Tracardi's server. All events on the page are batched and sent
   when the page completes loading. This approach helps reduce the number of network requests and enhances performance.
   However, there is a drawback: if you wish to dynamically send an event when, for example, someone clicks on an image
   or hovers the mouse, you must use on-demand event collection. This necessitates adding the "fire: true" option to
   the "window.tracker.track" function.

---
This answers also questions:
- How does Tracardi utilize a JavaScript snippet for event collection?