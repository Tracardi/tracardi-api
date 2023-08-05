# How to send event when I click something?

To bind an event to a button click, you can use the JavaScript code provided in the Tracardi documentation. First, you need to add an onClick event to the button, like this: 

```html
<button onClick="testClick()">Test click</button>
```

Then, you need to create a function that will send an event when the button is clicked. This function should be added to the JavaScript code, like this: 

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1});
  }
</script>
```

This code will record the event in the console, but it won't be sent to Tracardi by default. To trigger the event and send it to Tracardi immediately, you need to add the `fire` attribute with a value of `true` as a parameter to the window.tracker.track function, like this: 

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1}, {"fire": true}); // (1)
  }
</script>
```

This will send the event to Tracardi immediately.
