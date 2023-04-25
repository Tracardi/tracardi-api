# Javascript integrations

Tracardi provides a JavaScript snippet that allows seamless integration of any webpage with Tracardi for tracking and
personalization purposes. Follow the steps below to connect and configure the JavaScript snippet on your web page.

## Step 1: Connecting the JavaScript Snippet

To use the Tracardi JavaScript snippet, you need to paste it in the header of your web page. Here's an example of the snippet:

```html linenums="1"

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

Events are defined in a separate script. Below you may find an example of such script.

```javascript title="Example" linenums="1"
window.tracker.track("purchase-order", {"product": "Sun glasses - Badoo", "price": 13.45})
window.tracker.track("interest", {"Eletronics": ["Mobile phones", "Accessories"]})
window.tracker.track("page-view",{});
```

Events consist of an event type. Event type is any string that describes what happened. In our example we have 3
events: "purchase-order", "interest", "page-view".

!!! Caution

  The code with events must be placed after the configuration code. Otherwise, it will now work.

### Event type

Event type is a crucial aspect of defining events in Tracardi. It refers to the name that distinguishes events from each
other. For example, a purchase order event provides information about an order, while a page view event signifies a
viewed page.

Defining an appropriate event type is essential to ensure proper categorization and processing of events within
Tracardi. It allows you to effectively organize and analyze event data based on their type, which can aid in gaining
valuable insights and generating meaningful reports. 

#### Importance of Event Type

Event type serves as a unique identifier for events and helps differentiate them from one another. It enables you to
effectively manage and process events, as different events may require different handling or processing logic based on
their type.

When defining an event in Tracardi, you need to specify an event type that accurately represents the nature of the
event. For instance, if you are tracking purchase orders, you can define the event type as "purchase-order". Similarly,
if you are tracking page views, you can define the event type as "page-view".

### Events properties

In Tracardi, each event can have additional data that provides detailed information about the event. For example,
consider the event "interest" which sends data in the format {"Electronics": ["Mobile phones", "Accessories"]}.

Tracardi collects all events with their respective data and sends them as a single request to the Tracardi tracker
endpoint. This request is made when the web page is fully loaded, ensuring that all events and their associated data are
captured accurately.


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

To resolve this, create an event source in Tracardi and replace the string <your-resource-id-HERE> with the actual event source ID from Tracardi, as shown below:

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

