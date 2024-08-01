# I use commercial version and I do not see my widget

If you're using the commercial version of Tracardi and don't see your widget, it's important to understand how it
handles event processing. Commercial Tracardi typically processes events asynchronously, which means workflows run in
the background and the initial server response doesn't include workflow-defined details like widgets. This differs from
the open-source version, which processes events synchronously and requires the server to complete event processing
before sending a response.

To see your widget, you may need to adjust the processing mode from asynchronous to synchronous. This change is
necessary if you need immediate feedback, such as data or a widget display. To switch to synchronous processing, set
the `async` option to `false` in your tracking configuration:

```javascript
window.tracker.track(<event-type>, <properties>, { "async": false });
```

Add this in the options parameter of your tracking call to modify how events are handled.
