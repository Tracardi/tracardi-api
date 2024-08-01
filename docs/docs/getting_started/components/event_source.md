# Event source

In Tracardi, an event source is a defined entry point for collecting data. It specifies where and how data is captured,
and it plays a critical role in the data collection process. Here’s a detailed description of event sources in Tracardi:

## What is an Event Source?

An event source in Tracardi is a configuration that determines the origin and nature of the data being collected. It
serves as a gateway through which events, representing various user interactions and actions, enter the Tracardi system.
Key Components of an Event Source

* **Source Bridge**: Bridge defines how the data will be collected. This is kind of type of event source that specifies
  the nature and protocol of the data collection. Common types include REST API endpoints, webhooks, JavaScript
  tracking, and more. Each bridge defines a different method of data ingestion.

* **Source ID**: Each event source is assigned a unique identifier (ID) that is used to reference it within the Tracardi
  system. This
  ID is crucial for configuring integrations and ensuring data is routed correctly.

* **Configuration Details**: Name: A descriptive name for the event source to easily identify it; Description:
  Description of the source; Channel: Mobile, Web, CRM, Call Center, etc.; Bridge specific configuration: Queue Topic,
  etc.

## Purpose of Event Sources

* **Data Collection**: Event sources are fundamental for collecting data from various channels, including websites,
  mobile apps, CRM systems, and other platforms. They enable Tracardi to capture user interactions and other relevant
  data in real-time.

* **Data Source Identification**: They allow identification of the channel that the event came from for further
  processing and analysis.

* **Event Routing**: For certain event sources, you can specify how incoming events are processed within Tracardi. Some
  event sources may only collect data with a defined payload, which will be processed in a strictly defined manner
  within Tracardi.

## Setting Up an Event Source

* **Create an Event Source**: In the Tracardi GUI, navigate to the Inbound Traffic section and select Add New Source.
  Provide the necessary details,
  such as name, type, and channel.

* **Integration with JavaScript Snippet**: If using a web-based event source, integrate the JavaScript snippet into your
  web pages. This snippet will send events
  to the Tracardi event source.

* **Testing and Verification**: After setting up the event source, test it to ensure that data is being collected
  correctly. This involves triggering
  events from the configured source and verifying that they appear in the Tracardi system.

## Example Use Cases

* **Web Tracking**: Capturing page views, clicks, and form submissions from a website using the JavaScript tracking
  snippet.

* **Call Center Calls**: Collect all the interactions with your call center under the profile history.

* **Email Campaigns**: Tracking email opens and link clicks using redirect links and tracking parameters.

* **CRM Integration**: Collecting customer data from a CRM system through a REST API event source.

* **Webhook Integration with Other Systems**: Collect Slack messages, or Github Stars, or Filled forms, etc.

There are endless use cases how the data can be collected