# Tracker context

Event context in Tracardi allows you to extend the information about the __events__ by defining the scope of context data.
This context data can be used to pass additional information, such as browser metadata, system variables, etc.

!!! Caution

    When working with events context in Tracardi, it's important to understand that the context data refers to all 
    tracker events within a session, rather than a single event. The context data is saved in the session when it is 
    created and remains constant throughout the session, as data such as browser type or system used typically 
    does not change during a visitor's session on a website.

    However, it's worth noting that some context data, such as the page URL, may change from event to event within a 
    session. This dynamic data is sent in the event context, allowing you to capture and utilize it in your 
    workflows accordingly. Althouhg It is configured on the tracker level it will be attached to each event.

Configuration can be extended with *context* parameter, where you may define the scope of context data.

```javascript title="Example" linenums="1" hl_lines="10-16"
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
            location: false
        }
    }
}
```

Default context settings are:

```json
{
  "cookies": false,
  "storage": false,
  "screen": true,
  "page": true,
  "browser": true,
  "performance": false,
  "location": false
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

```json title="Example of event context"
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

# Tracker settings

Tracker settings turn on/off additional tracker features.

### Append profile ID to external links (Tagging links)

The tracking script has the capability to include the current profile ID, session ID, and source ID in the URL parameter, 
allowing for consistent profile ID persistence across domains that utilize the same Tracardi system. 

Please note that default behaviour without `passing of profile ID` enabled would be to create a random profile ID
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

