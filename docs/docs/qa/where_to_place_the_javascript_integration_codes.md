# Where to place javascript integration code?

When integrating JavaScript code for a REST API event source in a webpage, you'll need to place the code in the
appropriate sections of your HTML document. Here's a general guide on where to place the integration code:

1. First Part of Code (Header):
   The first part of the integration code, which is typically used for initialization or setup, should be placed in
   the `<head>` section of your HTML document. This ensures that the required scripts and configurations are loaded
   before the rest of the page content.

Here's an example of where you should place the first part of the code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Webpage Title</title>
    <!-- Place the first part of the integration code here -->
    <script> <!-- code HERE --> </script>
</head>
<body>
<!-- Your webpage content goes here -->
</body>
</html>
```

2. Second Part of Code (Particular Pages):
   The second part of the integration code, which is specific to certain pages or actions, should be placed in the
   relevant sections of your HTML where you want the events to be triggered and sent to Tracardi. This code is often
   placed within `<script>` tags at the bottom of the page, just before the closing `</body>` tag. This ensures that the
   page content is loaded first before the script executes.

Here's an example of where you should place the second part of the code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Webpage Title</title>
    <script src="path/to/your-first-part-code.js"></script>
</head>
<body>
<!-- Your webpage content goes here -->

<!-- Place the second part of the integration code within the script tag below -->
<script>
        // Your second part of the integration code here
        // This code will be specific to certain pages or actions
        // and will send events to Tracardi as intended.
    
</script>
</body>
</html>
```

In the code above, the second part of the integration code is placed within the <script> tags in the <body> section of
the HTML document. This ensures that the code is executed after the page content has been loaded. Remember to replace
the comment "Your second part of the integration code here" with the actual JavaScript code provided to you by Tracardi
for sending events.
