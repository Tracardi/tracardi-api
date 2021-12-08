# Web page JS integrations

## Connecting and configuring the script

Tracardi comes with Javascript snippet that integrates any webpage with Tracardi. In order to use it you must paste it
in your web page header. This is the example of the snippet:

```html

<script>
        const options = {
            tracker: {
                url: {
                    script: 'http://192.168.1.103:8686/tracker',
                    api: 'http://192.168.1.103:8686'
                },
                source: {
                    id: "<your-resource-id-HERE>"
                }
            }
        }

        !function(e){"object"==typeof exports&&"undefine...

    

</script>
```

If you refresh your page with the above javascript code you will notice that the response from tracardi will be like
this:

```
Headers:
Status: 401 Unauthorized

Body:
{"detail": "Access denied. Invalid source."}
```

This is because of the invalid source id that was not defined in the option.source.id section of the snippet. To obtain
source id create resource in Tracardi and then replace string ‘<your-resource-id-HERE>‘ with the resource id from
Tracardi, like this:

```html

<script>
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

        !function(e){"object"==typeof exports&&"undefined"!=ty...

    

</script>
```

Please notice that there is also the URL of Tracardi backend server. Please replace the IP e.g. 192.168.1.103 with the
address of your Tracardi server.

## Context data scope

Configuration can be extended with *context* parameter, where you may define the scope of context data. 

*Example*

```javascript
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

```json
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
Storage (localStorage) and session data is by default excluded. You can change it by explicitly flagging storage:true 
in the context configuration. 

*Caution* Sending cookies and localStorage data can lead to data explosion in Tracardi database. Each customer may have
different cookies and local data that will lead to the 1000 fields per record limit in elastic. This will stop writing new
sessions to the system.

## Sending events

Events are defined in a separate script. Below you may find an example of such script. 

```javascript
window.response.context.profile = true;
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]})
window.tracker.track("page-view",{});
```

Events consist of an event type. Event type is any string that describes what happened. In our example we have 3
events: "purchase-order", "interest", "page-view".

### Events data, properties

Each event may have additional data that describes the details of the event. For example, we have the event "interest"
and it sends data `{"Eletronics": ["Mobile phones", "Accessories"]}`

Tracardi collects all events and sends it as one request to the Tracradi tracker endpoint.

All events will be sent when page fully loads.

## Binding events to page elements

You can also bind events to page elements. To do that you will need to be sure that the page loads and every element of
the page is accessible.

To do that add the following configuration to options.

```javascript
listeners: {
    onContextReady: ({helpers, context}) => {
      // Code that binds events.
    }
}
```

The whole configuration should look like this.

```html

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

Then you can write a code that binds for example onClick event on a button to tracardi event.

This is the example code:

```javascript
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

```javascript
const btn0 = document.querySelector('#button')
```

Then using helpers binds onClick on that element to function:

```javascript
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

```javascript
const response = await helpers.track("page-view", {"page": "hello"});
```

And on response we make a string from JSON response and bind it as innerText of element with
id='response-to-custom-event'

## Wrap up

The whole configuration looks like this:

```html

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

```javascript
const btn0 = document.querySelector('#button')                 
helpers.addListener(btn0, 'mouseover', async ()=> {
    // Code
});
```

Helpers also have track method that let you send custom event to Tracardi at any time. 
