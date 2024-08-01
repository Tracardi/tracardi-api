# Advanced configurations

## Forcing Profile ID

Sometimes, your backend system might need to send a unique Profile ID to Tracardi. This can happen when your backend
system is working and needs to use that ID as the profile ID for Tracardi (e.g. PHPSESSID is used to store the profile
ID). This is helpful if your backend system already knows the profile ID and you want to share it with Tracardi. To do
this, you need to turn on the option for a fixed ID in the data collection settings, and then add the profile ID into
the tracking settings.

Here's an example:

```html title="Example" linenums="1" hl_lines="15-17"

<script>

    !function(e){"object"==typeof exports&&"undefine...  

    const options = {
        tracker: {
            url: {
                script: 'http://192.168.1.103:8686/tracker', 
                api: 'http://192.168.1.103:8686'
            },
            source: {
                id: "<your-event-source-id-HERE>" 
            },
            profile: {
                id: "<your-static-profile-id-HERE>" 
            }
        }
    }
</script>
```

!!! Notice

    It's important to note that this will send the provided profile ID regardless of whether a profile ID is already stored
    in the browser's local storage. If event source si not configured to allow static profile ID then System will try
    to load profile with provided ID - it will most probably fail and then it will generate the random ID. Please do
    not use this feature with events sources that has disabled static profile processing in events source. 

!!! Warning

    Please be aware that sending a profile ID that's easy to guess can be a security risk. Attackers can potentially guess
    the ID and try to corrupt its data. Always use IDs like UUID4 to ensure security.

!!! Notice

    This feature is available from version 0.8.1 up.

## Capturing Tracker Response

Tracardi allows you to capture the response from event collector, which can be useful for customizing page content based on customer
segments or utilizing data returned from workflows. In the provided example, the event response is captured using the
window.onTracardiReady event and accessed through the context.response object. For example:

```javascript title="Example" 
 // Change page if has response custom.text
 window.onTracardiReady.bind( ({tracker, helpers, context, config}) => {
     if(context?.response?.custom?.text) {
         const customText = document.getElementById('custom')
         customText.innerText = context?.response?.custom?.text
     }
 })
```

In the above example, the context.response.custom.text value is accessed from the response and used to update the
content of an HTML element with the id attribute of 'custom'. This allows you to dynamically change the page content
based on the data returned from Tracardi workflows.

## Binding Page Elements

You can also bind events to page elements. To do that you will need to be sure that the page loads and every element of
the page is accessible.

To do that bind the function to `window.onTracardiReady` property.

```javascript title="Example" linenums="1"
window.onTracardiReady.bind( ({helpers, context, config, tracker}) => {
      // Code that binds events.
    }
});
```

The whole configuration should look like this.

```html title="Example" linenums="1"

<script>
        !function(e){"object"==typeof exports&&"undefined\...

        window.onTracardiReady.bind( ({helpers, context, config, tracker}) => {
              // Code that binds events.
            }
        });

        const options = {
            tracker: {
                url: {
                    script: 'http://192.168.1.103:8686/tracker',
                    api: 'http://192.168.1.103:8686'
                },
                source: {
                    id: "ee2db027-46cf-4034-a759-79f1c930f80d"
                }
            }
        }
        
  </script>
```

The above example will run on every page after the events are triggered. It will not run if TRACARDI did not respond.

The function have the following parameters.

* *helpers* - this is a reference to class that will allow you to raise another events
* *context* has the response from Tracardi to you initial events. It will have profile data, and if configured debug
  information.
* *config* - it is the tracker config as defined in options
* *tracker* - it is tracker object.

## OnTracardiReady triggered on selected page

You can bind functions to `windows.OnTracardiReady` on selected pages together with track events. Then it will be
executed only on selected pages.

```javascript
window.tracker.track("page-view",{}); // (1)
window.onTracardiReady = ({tracker, helpers, context, config}) => {
    // Code
}
```

1. Set tracks first. Then bind a function.

### Binding events to page elements

Then you can write a code that binds for example onClick event on a button to tracardi event.

This is the example code that you can bind to `window.onTracardiReady`

```javascript title="Example" linenums="1"
({helpers, context}) => {
    const btn0 = document.querySelector('#button')

    helpers.onClick(btn0, async ()=> {
        const response = await helpers.track("page-view", {"page": "hello"});

        if(response) {
            const responseToCustomEvent = document.getElementById('response-to-custom-event');
            responseToCustomEvent.innerText = JSON.stringify(response.data, null, " ");
            responseToCustomEvent.style.display = "block"
        }
    });
}
```

It looks for the element with id="button"

```javascript title="Example" linenums="1"
const btn0 = document.querySelector('#button')
```

Then using helpers binds onClick on that element to function:

```javascript title="Example" linenums="1"
async ()=> {
        // Send event to tracardi
        const response = await helpers.track("page-view", {"page": "hello"});

        if(response) {
            const responseToCustomEvent = document.getElementById('response-to-custom-event');
            responseToCustomEvent.innerText = JSON.stringify(response.data, null, " ");
            responseToCustomEvent.style.display = "block"
        }
    }
``` 

Inside the function we send the event to Tracardi:

```javascript title="Example" linenums="1"
const response = await helpers.track("page-view", {"page": "hello"});
```

And on response we make a string from JSON response and bind it as innerText of element with
id='response-to-custom-event'

## Wrap up

The whole configuration looks like this:

```html title="Whole code" linenums="1"
<script>

    // Compiled code must be always in the first line
    
    !function(e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):("undefined"!=typeo...

    // Configure tracker

    const options = {
        tracker: {
            url: {
                script: 'http://192.168.1.103:8686/tracker',
                api: 'http://192.168.1.103:8686'
            },
            source: {
                id: "ee2db027-46cf-4034-a759-79f1c930f80d"
            }
        }
    }
    
    // Bind some function when TRACARDI responds

    window.onTracardiReady.bind(({helpers, context}) => {
        const btn0 = document.querySelector('#button')
    
        helpers.onClick(btn0, async ()=> {
            const response = await helpers.track("page-view", {"page": "hello"});
    
            if(response) {
                const responseToCustomEvent = document.getElementById('response-to-custom-event');
                responseToCustomEvent.innerText = JSON.stringify(response.data, null, " ");
                responseToCustomEvent.style.display = "block"
            }
        });
    });

</script>
```

## Tracardi helpers

You probably noticed that we use helpers to bind events. We used onClick method to bind to click event. You might need
to bind to other than click event. To do that use addEventListener:

```javascript title="Example" linenums="1"
const btn0 = document.querySelector('#button')                 
helpers.addListener(btn0, 'mouseover', async ()=> {
    // Code
});
```

Helpers also have track method that let you send custom event to Tracardi at any time.

This is how you can use it:

```javascript title="Example" linenums="1"
const response = await helpers.track("new-page-view", {"page": "hello"});
```