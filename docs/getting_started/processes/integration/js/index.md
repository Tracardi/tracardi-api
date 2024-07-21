# Javascript integrations

Tracardi provides a JavaScript snippet that allows seamless integration of any webpage with Tracardi for tracking and
personalization purposes. 

It is crucial to first understand the concept of [tracker payload](../../../definitions/track_payload.md) and [API integrations](../api/index.md) because the JavaScript snippet is
browser code that relies on API integration and the tracker payload schema to send data.

# Integrating Tracardi with web page.

Follow the steps below to connect and configure the JavaScript snippet on your web page.

## Step 1: Connecting the JavaScript Snippet

To use the Tracardi JavaScript snippet, you need to create an [event source](../../../components/event_source.md) with [bridge](../../../components/bridge.md) Rest API. Then click on the event
source and select tab `Use & Javascript`. Then copy the Javascript code displayed in GUI to the header of your web page.
Here's an example of the snippet:

```html linenums="1" title="Example of a Javascript code"

<script>

    !function(e){"object"==typeof exports&&"undefine...  // (1)

    const options = {
        tracker: {
            url: {
                script: 'http://192.168.1.103:8686/tracker', 
                api: 'http://192.168.1.103:8686'
            },
            source: {
                id: "<your-event-source-id-HERE>" // (2)
            }
        }
    }
</script>
```

1. Compiled javascript code must be the first line in the script.
2. You `event source id` should be copied here. Event source can be found in Inbound traffic in Tracardi GUI.

## Step 2: Sending events via Javascript

Events are defined in a separate script. 

```javascript title="Example of events" linenums="1"
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]})
window.tracker.track("page-view",{});
```

Events consist of an event type. Event type is any string that describes what happened. In our example we have 3
events: `purchase-order`, `interest`, `page-view`.

!!! Caution

    The code with events must be placed after the configuration code. Otherwise, it will now work.

For a [detailed description of event trigger function see this page](event_trigger.md).

## Step 3: Refreshing the Page and Verifying the Response

After refreshing your web page with the JavaScript code, you may notice a response from Tracardi indicating "Access
denied. Invalid source." This is because the event source ID was not defined in the __tracker.source.id__ section of the
snippet.

```
Headers:
Status: 401 Unauthorized

Body:
{"detail": "Access denied. Invalid source."}
```

To resolve this, create an event source in Tracardi and replace the string <your-resource-id-HERE> with the actual event
source ID from Tracardi, as shown below:

```html linenums="1"

<script>
    !function(e){"object"==typeof exports&&"undefined"!=ty... // (3)
    
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

</script>
```

1. Correct `event source id`.
2. Replace IP with the IP of Tracardi API. Please mind the port and correct it as well
3. The code here is truncated for the purpose of more readable documentation.

Please notice that there is also the URL of Tracardi backend server. Please replace the IP e.g. `192.168.1.103` with the
address of your Tracardi server.

# Additional configuration

## Configuration of event context scope

Tracardi automatically adds a context to the event. The scope of the context can be configured. 
Configuration can be extended with *context* parameter, where you may define the scope of context data.

!!! Caution

    When working with event's context in Tracardi, it's important to understand that the context data refers to all 
    tracker events within a session, rather than a single event. The context data is saved in the session when it is 
    created and remains constant throughout the session, as data such as browser type or system used typically 
    does not change during a visitor's session on a website.

    However, it's worth noting that some context data, such as the page URL, may change from event to event within a 
    session. This dynamic data is sent in the event context. Although It is configured on the tracker level it 
    will be attached to each event.

```javascript title="Example of tracker configuration with scope of event context" linenums="1" hl_lines="10-19"
    const options = {
      tracker: {
        url: {
            script: '//localhost:8686/tracker',
            api: '//localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        context: {
            cookies: false,
            storage: false,
            browser: true,
            page: true,
            screen: true,
            performance: false,
            location: false,
            utm: true
        }
    }
}
```

If you omit the context configuration it will be set to the default value:

```json title="Default Context Values"
{
  "cookies": false,
  "storage": false,
  "screen": true,
  "page": true,
  "browser": true,
  "performance": false,
  "location": false,
   "utm": true
}
```

By default, the following session context data will be sent to Tracardi:

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

!!! Caution

    Sending cookies and localStorage data can lead to data explosion in Tracardi database. Each customer may have
    different cookies and local data that will lead to the 1000 fields per record limit in elastic. This will stop writing
    new sessions to the system.

### Customer GEO location

By setting the __context.location__ to true, system will try to catch geo location on client side. 

### Event performance metrics

If you set `tracker.context.performance` to TRUE in tracker context configuration the result from __window.performance.getEntriesByType("
navigation")__ will be sent as event context.

```json title="Example of event performance context"
{
  "context": {
    "performance": {
      "name": "http://localhost:63343/analytics-js-tracardi/index.html",
      "entryType": "navigation",
      "startTime": 0,
      "duration": 0,
      "initiatorType": "navigation",
      "nextHopProtocol": "http/1.1",
      "workerStart": 0,
      "redirectStart": 0,
      "redirectEnd": 0,
      "fetchStart": 20,
      "domainLookupStart": 101,
      "domainLookupEnd": 101,
      "connectStart": 101,
      "connectEnd": 102,
      "secureConnectionStart": 0,
      "requestStart": 102,
      "responseStart": 102,
      "responseEnd": 102,
      "transferSize": 9394,
      "encodedBodySize": 9089,
      "decodedBodySize": 9089,
      "serverTiming": [],
      "unloadEventStart": 106,
      "unloadEventEnd": 107,
      "domInteractive": 158,
      "domContentLoadedEventStart": 160,
      "domContentLoadedEventEnd": 161,
      "domComplete": 0,
      "loadEventStart": 0,
      "loadEventEnd": 0,
      "type": "reload",
      "redirectCount": 0
    }
  }
}
```

### Event UTM collection

#### What is UTM?

UTM (Urchin Tracking Module) parameters are used to track the effectiveness of online marketing campaigns across traffic
sources and publishing media. They are appended to URLs and help in identifying the source, medium, and campaign name
associated with the marketing efforts. Common UTM parameters include:

* **utm_source**: Identifies the source of the traffic (e.g., Google, newsletter).
* **utm_medium**: Identifies the medium (e.g., email, CPC).
* **utm_campaign**: Identifies the specific campaign (e.g., spring_sale).
* **utm_term**: Identifies the paid keywords (used for paid search).
* **utm_content**: Differentiates similar content or links within the same ad (e.g., banner, link).

#### Turn on UTM collection

To turn UTM collection you need to configure it in tracker script.

```javascript title="Example of tracker configuration with UTM collection" linenums="1" hl_lines="10-12"
    const options = {
      tracker: {
        url: {
            script: '//localhost:8686/tracker',
            api: '//localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        context: {
            utm: true
        }
    }
}
```

UTM data will be saved in event and session UTM fields.

## Append profile ID to external links (Tagging links)

The tracking script has the capability to include the current profile ID, session ID, and source ID in the URL
parameter, allowing for consistent profile ID persistence across domains that utilize the same Tracardi system. It
uses [Parametrized Links](../param/index.md) feature to pass the Profile ID across different web sites.


!!! Note 

      Please note that default system behaviour without `passing of profile ID in Link` enabled would be to create a random profile ID
      if customer never visited the page before. And later merge the profile if customer provides data that can be used 
      for this. 

To enable this functionality, you can add the following code: `trackExternalLinks: ['example.com', 'tracardi.com']`. 
This will automatically update all `A.href` links on the page 
with the `__tr_pid`, `__tr_src` parameter, which will contain the current profile ID, source ID respectively, if
the A.href URL end with any of the defined domains in `trackExternalLinks`. In our example it is 'example.com' and , 
'tracardi.com'.

```javascript title="Example" linenums="1" hl_lines="10-12"
    const options = {
      tracker: {
        url: {
            script: '//localhost:8686/tracker',
            api: '//localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        settings: {
          trackExternalLinks: ['example.com', 'tracardi.com']
        }
    }
}
```

Tracardi recognize these params and saves them in `session.context` and replaces profile ID with the profile ID
referenced in `__tr_pid`

!!! Warning

    Profile must exist in Tracardi to be passed from domain to domain. If profile does not exist then
    new profile ID will be generated and a Javascript warning will be logged: `Referred Tracardi Profile Id
    {referred_profile_id} is invalid`.

!!! Notice

    This feature is available from version 0.8.1 up.

```json
{
  "context": {
    "tracardi": {
      "pass": {
        "profile": "0adfd4c8-36eb-40cd-9350-5df37706286a",
        "source": "d15aaf64-90ff-4c72-9d93-e7851c326127",
        "session": "9cb9a69b-e657-47dc-85f6-791ebc4b4822"
      }
    }
  }
}
```

Where possible system will use this information to merge profiles between devices and browsers. 

!!! Tip

    The script utilizes an underlying technique that involves creating a POST payload for the tracker, with 
    parameters such as `__tr_pid`, `__tr_src`. The payload contains data sent in a specific context, 
    formatted as follows in JSON:
    
    ```json
    {
      "source": {
        "id": "d15aaf64-90ff-4c72-9d93-e7851c326127"
      },
      "context": {
        "tracardi": {
          "pass": {
            "profile": "0adfd4c8-36eb-40cd-9350-5df37706286a",
            "source": "d15aaf64-90ff-4c72-9d93-e7851c326127"
          }
        }
      },
      "profile": {
        "id": "0adfd4c8-36eb-40cd-9350-5df37706286a"
      },
      "session": {
        "id": "3a18978e-1d74-4382-8e50-f0b8ae3c2d55"
      },
      "options": {},
      "events": [ ... ]
    }
    ```

    This technique can be used also to reference profile ID from browser to device. 
    However you will need a find a way to pass the refered profile ID, session ID, and source ID to your mobile 
    device when the app is opened, and the first `/track` payload should include the refered IDs. The same 
    will also work with other systems. 

To disable params `__tr_pid`, `__tr_src` and turn off session context, set `tracardiPass` to `false` in 
tracker context:

```javascript title="Example" linenums="1" hl_lines="10-12"
    const options = {
      tracker: {
        url: {
            script: '//localhost:8686/tracker',
            api: '//localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        context: {
            tracardiPass: false
        }
    }
}
```


### Respect Do Not Track (DNT) browser setting

Do Not Track (DNT) is a web browser setting that adds a signal to the browser, telling websites that the user don’t want
to be tracked. By 2011, DNT had been adopted by all the major browsers, but it’s not enforceable. That means its default
value is set to track the user.

You can respect the browser setting and do not to track the user. If you decide to do this Tracardi will not load the
tracking script if the user sets DNT. To respect the DNT set `respectDoNotTrack: true`
in settings section of tracker options.

```javascript title="Example" linenums="1" hl_lines="10-12"
    const options = {
      tracker: {
        url: {
            script: '//localhost:8686/tracker',
            api: '//localhost:8686'
        },
        source: {
            id: "3ee63fc6-490a-4fd8-bfb3-bf0c8c8d3387"
        },
        settings: {
          respectDoNotTrack: true
        }
    }
}
```

If the `respectDoNotTrack` is missing in the settings than Tracardi sets default setting and loads tracking script.

## Auto Events

Auto events and triggers provide a simple approach to managing event handling in web pages. This documentation
outlines the benefits of using auto events, describes how they are configured, and provides guidance on integrating
triggers with HTML elements.

At a high level, the primary benefit of using auto events is the centralization of event and trigger definitions.
Instead of scattering event handling logic throughout the page, auto events allow for the consolidation of these
definitions in one place. This results in improved code organization, readability, and maintainability.

### Key Concepts

1. **Auto Events** - these events are triggered automatically upon page load.
2. **Auto Triggers** - these triggers are activated in response to user interactions with the page.

### Configuration

Auto events and triggers are configured using a structured format.

Following is an example configuration:

```javascript title="Configuration Example" hl_lines="10-20"
const options = {
    tracker: {
        url: {
            script: 'http://192.168.1.103:8686/tracker', 
            api: 'http://192.168.1.103:8686'
        },
        source: {
            id: "<your-event-source-id-HERE>"
        },
        auto: { // (1)
                events: [
                        ["increase-interest", {"interest": "laptops", "value": 1}],
                        ["increase-interest", {"interest": "systems", "value": 2}],
                        ["page-view", {"category": "laptops"}]
                ],
                triggers: [
                        {tag:"product", trigger:'onVisible', data: {event: 'image-viewed'}},
                        {tag:"title", trigger:'onTextSelect', data: {event: 'text-selected'}
                ]
        }

}
```

Note:

* (1) - Optional `auto` configuration extends the track options.

### Usage with Triggers and HTML Elements

In addition to configuring auto events and triggers in your JavaScript code, you can integrate them with HTML elements
using the data-tracardi-tag attribute.

This allows you to specify which elements on the page should trigger events based on user interactions.

#### Steps to Implement:

##### 1 - Define Triggers:

Configure auto triggers in your JavaScript code as described in the previous section.

##### 2 - Add data-tracardi-tag Attribute:

Identify the HTML elements on your page that should trigger events based on user interactions.

Add the data-tracardi-tag attribute to these elements and assign a value corresponding to the desired trigger tag
defined in your JavaScript configuration.

```html title="Example"
<div data-tracardi-tag="product"> <!-- Content of the div --> </div>
```

##### 3 - Trigger Events:

When the specified user interaction or condition associated with the trigger occurs on the tagged HTML element, the
corresponding event defined in your JavaScript configuration will be triggered.

#### Notes:

1. The value assigned to the data-tracardi-tag attribute should match the tag property specified in your auto trigger
   configuration.
2. You can customize the data-tracardi-tag value based on your application's specific requirements and naming
   conventions.
3. By integrating triggers with HTML elements using the data-tracardi-tag attribute, you can easily specify which
   elements should activate events based on user interactions, enabling flexible and targeted event tracking on your web
   pages.





