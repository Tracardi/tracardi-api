# REST API Bridge in Tracardi

The REST API Bridge in Tracardi is designed to facilitate data collection via HTTP requests. It is one of the primary
bridges used for structured data collection, providing a straightforward method for integrating external systems with
Tracardi.

## How the REST API Bridge Works?

- **Endpoint and Method**:  The REST API Bridge uses a standard endpoint `/track` and the HTTP POST method to collect
  data. This endpoint is
  configured to receive event data from external systems.

```commandline title="Example Endpoint"
POST http://your-tracardi-url/track
```

- **Data Structure**: Data sent to the REST API Bridge must be structured in JSON format. This JSON payload includes.
  metadata plus a list of event for particular profile.

```json title="Example Payload"
{
  "events": [
    {
      "type": "page-view",
      "properties": {
        "url": "https://example.com",
        "title": "Homepage"
      }
    }
  ],
  "session": {
    "id": "session-id"
  },
  "profile": {
    "id": "profile-id"
  }
}
```

- **Configuration and Setup**: The REST API Bridge does not require additional configuration beyond setting up the event
  source in Tracardi. Here’s how
  to set it up:

   - **Create an Event Source**:
      - Navigate to the Inbound Traffic section in the Tracardi GUI.
      - Click on Add New Source.
      - Provide a name, type, and channel for the event source.
      - Select the REST API Bridge as the method of data collection.

   - **Integration with External Systems**:
      - Configure your external system to send HTTP POST requests to the [/track endpoint](../../processes/integration/api/index.md#track-endpoint) of your Tracardi instance.
      - Ensure the payload follows the JSON structure required by Tracardi.

- **Event Processing**:  Once the data is received by the /track endpoint, Tracardi processes the event through
  several stages: Validation:, Mapping, Identity Resolution, Event Storage, Workflow Execution. Some steps may be
  executed in parallel in commercial version of Tracardi.

- **Example Integration**:  To illustrate, here’s how you might configure an external application to send data to
Tracardi using the REST API Bridge.

```bash title="Example cURL Command"

curl -X POST http://your-tracardi-url/track \
-H "Content-Type: application/json" \
-d '{
   "events": [
      "type": "purchase",
      "properties": {
         "product": "Laptop",
         "price": 1200.00
      }
    ],
    "source": {
      "id": "source-12345"
    },
    "profile": {
      "id": "profile-67890"
    }
}'
```

## Benefits of Using REST API Bridge

Simplicity: Easy to set up and use with minimal configuration.
Flexibility: Can be integrated with various systems and platforms that support HTTP POST requests.
Real-Time Data Collection: Enables real-time data ingestion and processing.
Scalability: Suitable for collecting data from high-traffic applications.

