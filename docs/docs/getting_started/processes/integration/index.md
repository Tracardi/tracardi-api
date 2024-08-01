# Integration

Integration in Tracardi refers to the process of connecting external systems, websites, and databases to Tracardi,
enabling data exchange and interaction. This process ensures that data from various sources can be collected, and
processed.

## Integration Types

### Integrations via API

1. **API Calls**:
    - **[Track Endpoint](api/index.md)** - Tracardi supports integration with external systems through APIs. This involves setting up API endpoints to receive data from third-party applications or to send processed data and insights back to these applications.
    - **[Webhook Endpoint](webhook/index.md)** - Tracardi supports integration via webhooks, which is an endpoint that does not require a predefined data schema.

2. **[Javascript](js/index.md)**:
    - This type of integration allows for the automatic event ingestion from the web page. Javascript snippet uses [Track Endpoint](api/index.md).

Both methods use the Tracardi API.

### Integrations via URL

1. **[Redirected Links](redirect/index.md)**: This method involves creating
  special links that, when clicked, send information to Tracardi about the user and then redirect them to a specific page. The information is stored within the link itself.

2. **[Parameterized Links](param/index.md)**: The second method involves adding
  a parameter `__tr_pid` to an existing link. This parameter contains user information. When user visits the target
  page, the tracking script, that must exist on the target page, sends an event to Tracardi and use the
  parameter `__tr_pid` to identify the customer. 

Both methods are similar, but they differ in who sends the event to the system. In Redirected Links, Tracardi handles
the event since the link is within the system. In the second method, the script located at the target page is
responsible for sending the event.

There could be other integration types when different [bridges](../../components/bridge.md) are used.