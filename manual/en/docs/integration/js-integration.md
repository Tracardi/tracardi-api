# Web page JS integrations

## Connecting and configuring the script

Tracardi comes with Javascript snippet that integrates any webpage with Tracardi. In order to use it you must paste it
in your web page header. This is the example of the snippet:

```html linenums="1"

<script>
        const options = {
            tracker: {
                url: {
                    script: 'http://192.168.1.103:8686/tracker', 
                    api: 'http://192.168.1.103:8686'
                },
                source: {
                    id: "<your-resource-id-HERE>" // (1)
                }
            }
        }

        !function(e){"object"==typeof exports&&"undefine...
</script>
```

1. You `event source id` should be copied here.

If you refresh your page with the above javascript code you will notice that the response from tracardi will be like
this:

```
Headers:
Status: 401 Unauthorized

Body:
{"detail": "Access denied. Invalid source."}
```

This is because of the __invalid source id__ that was not defined in the `option.source.id` section of the snippet. To obtain
source id create event source in Tracardi and then replace string ‘<your-resource-id-HERE>‘ with the source id from
Tracardi, like this:

```html linenums="1"
<script>
        const options = {
            tracker: {
                url: {
                    script: 'http://192.168.1.103:8686/tracker', // (2)
                    api: 'http://192.168.1.103:8686'
                },
                source: {
                    id: "ee2db027-46cf-4034-a759-79f1c930f80d" // (1)
                }
            }
        }

        !function(e){"object"==typeof exports&&"undefined"!=ty... // (3)
</script>
```

1. Correct `event source id`.
2. Replace IP with the IP of Tracardi API. Please mind the port and correct it as well
3. The code here is truncated for the purpose of more readable documentation.

Please notice that there is also the URL of Tracardi backend server. Please replace the IP e.g. `192.168.1.103` with the
address of your Tracardi server.

## Context data scope

Configuration can be extended with *context* parameter, where you may define the scope of context data.

```javascript title="Example" linenums="1" hl_lines="10-16"
    const options = {
      tracker: {
        url: {
            script: 'http://localhost:8686/tracker',
            api: 'http://localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        context: {
            browser: true,
            page: true,
            session: false,
            storage:true,
            screen: true
        }
    }
}
```

By default, the following context data will be sent to Tracardi:

```json title="Example" linenums="1"
{
  "context": {
    "time": {
      "local": "12/8/2021, 12:50:55 AM",
      "tz": "Europe/Warsaw"
    },
    "browser": {
      "local": {
        "browser": {
          "name": "Netscape",
          "engine": "Gecko",
          "appVersion": "5.0 (X11)",
          "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
          "language": "en-US",
          "onLine": true,
          "javaEnabled": false,
          "cookieEnabled": true
        },
        "device": {
          "platform": "Linux x86_64"
        }
      }
    },
    "page": {
      "local": {
        "url": "http://localhost:8686/tracker/",
        "path": "/tracker/",
        "hash": "",
        "title": "Test page",
        "referer": {
          "host": null,
          "query": null
        },
        "history": {
          "length": 10
        }
      }
    },
    "screen": {
      "local": {
        "width": 1835,
        "height": 1032,
        "innerWidth": 1835,
        "innerHeight": 928,
        "availWidth": 1835,
        "availHeight": 1013,
        "colorDepth": 24,
        "pixelDepth": 24
      }
    }
  }
}
```

It consists of browser data, screen data and page data. It can be extended with cookies and local storage data.
Storage (localStorage) and session data is by default excluded. You can change it by explicitly flagging storage:true in
the context configuration.

*Caution* Sending cookies and localStorage data can lead to data explosion in Tracardi database. Each customer may have
different cookies and local data that will lead to the 1000 fields per record limit in elastic. This will stop writing
new sessions to the system.

## Sending events

Events are defined in a separate script. Below you may find an example of such script.

```javascript title="Example" linenums="1"
window.response.context.profile = true; //(1)
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]})
window.tracker.track("page-view",{});
```

1. This line tells tracardi to return profile data with the response. 

Events consist of an event type. Event type is any string that describes what happened. In our example we have 3
events: "purchase-order", "interest", "page-view".

### Events data, properties

Each event may have additional data that describes the details of the event. For example, we have the event "interest"
and it sends data `{"Eletronics": ["Mobile phones", "Accessories"]}`

Tracardi collects all events and sends it as one request to the Tracradi tracker endpoint.

All events will be sent when page fully loads.

### Sending event on demand

Events can be sent immediately when parameters fire is set to true.


```javascript title="Example" linenums="1"
window.response.context.profile = true;  //(2)
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]}, {"fire": true}) //(1)
window.tracker.track("page-view",{});
```

1. This event will fire immediately.
2. This line tells tracardi to return profile data with the response. 

The event "interest" will be sent immediately, because of `{"fire": true}`.

## Handling response from Tracardi

You can also bind events to page elements. To do that you will need to be sure that the page loads and every element of
the page is accessible.

To do that add the following configuration to options.

```javascript title="Example" linenums="1"
listeners: {
    onContextReady: ({helpers, context}) => {
      // Code that binds events.
    }
}
```

The whole configuration should look like this.

```html title="Example" linenums="1"

<script>
        const options = {
            listeners: {
                onContextReady: ({helpers, context}) => {
                    // Code that binds events.
                },
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

        !function(e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):("undefined"!=typeo...
  </script>
```

The *onContextReady* method will run after the events are triggered. It will not run if the events are not defined.

The parameters have the following meaning.

* *helpers* - this is a reference to class that will allow you to raise another events
* *context* has the response from Tracardi to you initial events. It will have profile data, and if configured debug
  information.

You can configure how much data the server should return in the response to event track.

If you woul like to receive the full profile remember to set:

`window.response.context.profile = true;`

It is wise not to receive the full profile when you do not need it.

### Binding events to page elements

Then you can write a code that binds for example onClick event on a button to tracardi event.

This is the example code:

```javascript title="Example" linenums="1"
onContextReady: ({helpers, context}) => {
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

### Binding directly to page elements

There is another way of binding page elements. You may want to add a onClick event like this. You will not have access
to context data, such as profile.id, etc.

```html
<button onClick="testClick()">Test click</button>
```

Where the **testClick** function sends an event.

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1});
  }
</script>
```

When you click the **Test click** button then you will see the event being recorded in console.

```
[Tracker] Event track 
Object { type: "track", event: "page-view", properties: {…}, options: {}, userId: null, anonymousId: "642aa4a6-9a48-4c08-8fd5-f0772415c824", meta: {…} }
```

But it is not sent to Tracardi. This event is collected but never triggered. To trigger an event add fire attribute
equal to true as a param to window.tracker.track.

```html title="Example" linenums="1"
<script>
  function testClick() {
     window.tracker.track("page-view", {"view": 1}, {"fire": true});
  }
</script>
```

## Wrap up

The whole configuration looks like this:

```html title="Whole code" linenums="1"
<script>
         const options = {
             listeners: {
                 onContextReady: ({helpers, context}) => {
                     const btn0 = document.querySelector('#button')
                 
                     helpers.onClick(btn0, async ()=> {
                         const response = await helpers.track("page-view", {"page": "hello"});
                 
                         if(response) {
                             const responseToCustomEvent = document.getElementById('response-to-custom-event');
                             responseToCustomEvent.innerText = JSON.stringify(response.data, null, " ");
                             responseToCustomEvent.style.display = "block"
                         }
                     });
                 },
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
 
         !function(e){"object"==typeof exports&&"undefined"!=typeof module?module.exports=e():"function"==typeof define&&define.amd?define([],e):("undefined"!=typeo...
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


## Beacon tracks