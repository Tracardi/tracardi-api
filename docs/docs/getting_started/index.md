# Tracardi Getting Started

## What is Tracardi

Tracardi is a Customer Data Platform (CDP) designed to collect, analyze, and act on customer data. It provides tools for
managing and leveraging customer information to improve engagement and drive business growth. Here’s a detailed
explanation of Tracardi and its purposes:
What is Tracardi?

Tracardi is an open-source Customer Data Platform (CDP) that consolidates customer data from various sources, processes
this data, and enables businesses to create personalized customer experiences. It integrates seamlessly with websites,
applications, and other platforms to gather user interactions, profile data, and behavioral data.
Purpose of Installing Tracardi

The primary purposes of installing Tracardi include:

* **Data Collection and Integration**:
  Unified Data Repository: Tracardi collects data from multiple touchpoints such as websites, mobile apps, and CRM
  systems, storing it in a unified repository.
  Real-Time Data Processing: It processes data in real-time, allowing businesses to respond to customer actions as they
  happen.

* **Customer Profiling**:
  360-Degree View: Tracardi builds comprehensive customer profiles by combining data from various sources, giving a
  360-degree view of each customer.
  Identity Resolution: It resolves customer identities across different channels, ensuring accurate and consistent data.

* **Personalization and Engagement**:
  Tailored Experiences: Tracardi enables personalized marketing and communication by leveraging detailed customer
  profiles and behaviors.
  Automated Workflows: It supports the creation of automated workflows to trigger personalized messages, offers, and
  content based on customer actions.

* **Analytics and Insights**:
  Behavioral Analysis: Tracardi analyzes customer behavior to identify patterns, preferences, and trends.
  Segmentation: It segments customers into different groups based on various criteria, allowing targeted marketing
  efforts.

* **Data Orchestration**:
  Integration with External Systems: Tracardi can route processed data to external systems like CRM, marketing
  automation platforms, and data warehouses.
  Data Enrichment: It enhances raw data with additional context and information, improving its value for
  decision-making.

## Getting Started

To start collecting data in Tracardi, you need to set up the system, integrate it with your website or application, and
configure event sources and event tracking. Here's a step-by-step guide to get you started:

### 1. Install Tracardi

You need to have [Tracardi installed](../installation/index.md) and running. This can be done using Docker, Helm, or directly
from the source code. Ensure that all necessary components, such as the backend, frontend, and optional modules, are
installed.

### 2. Configure Event Sources

Event sources are the points where data enters Tracardi. You need to define these sources in the Tracardi system to
start collecting data from them.

* **Creating an Event Source**: Go to the Tracardi GUI, navigate to Inbound Traffic, and add a new event source. You'll
  need to provide details such as the name, type, and URL of the event source.

### 3. Integrate Tracardi JavaScript Snippet

To collect data from your website, you need to integrate the Tracardi JavaScript snippet into your web pages. Add the
JavaScript Snippet. You can find the snippet by clicking the event source and selecting `Use & Javascript` Tab:

```html title="Example configuration snippet, that should be placed on all pages"

<script>
    !function(e){"object"==typeof exports&&"undefined"!=typeof module..
</script>
<script>
    const options = {
        tracker: {
            url: {
                script: 'http://your-tracardi-url/tracker',
                api: 'http://your-tracardi-url'
            },
            source: {
                id: "<your-event-source-id>"
            }
        }
    }
</script>
```

!!! Tip

    Do not forget to replace your-tracardi-url with the URL of your Tracardi API server and your-event-source-id with the ID of your event source.

### 4. Send Events via JavaScript

Define and send events from your web pages using JavaScript. Events can represent various user actions such as page
views, clicks, form submissions, etc. Events properties are the data that is associated with the event, e.g. page url,
form data, etc.

```javascript title="Example snippet for data collection"
    window.tracker.track("page-view", {
      "url": window.location.href, 
      "title": document.title, 
      "category": "product details"
    });
    window.tracker.track("button-click", {
      "button-id": "subscribe-button"
    });
```

### 5. Verify Integration

After adding the JavaScript code and sending events, verify that the data is being collected properly in Tracardi.

* **Check Event Data**: Navigate to the Tracardi GUI and check the Events section to see if the events from your web
  pages are being captured. Data should appear withing 3 to 5 seconds.

### 6. Configure Workflows

Workflows define how events are processed in Tracardi. You can set up workflows to act on the collected
data. Workflows are not necessary to collect user data. They can automate the customer journey and allow messaging user
or personalizing their customer journey.

* **Create Workflows**: Go to the Processing section, create a new workflow, and define the nodes and actions based on
  your requirements.

If you would like more details about Tracardi, please follow these documents:

* **[Installation](../installation/index.md)**: How to install Tracardi
* **[Core elements](core_concepts.md)**
    * **[Tracardi Components](components/index.md)**: Data objects used in Tracardi.
    * **[Tracardi Definitions](definitions/index.md)**: Definitions used in Tracardi.
    * **[Tracardi Processes](processes/index.md)**: Processes in Tracardi
    * **[Tracardi Codings](codings/index.md)**: Processes in Tracardi
