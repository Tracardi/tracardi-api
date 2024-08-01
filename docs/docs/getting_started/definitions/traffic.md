### Traffic

Traffic refers to all the data that is sent to and from the Tracardi system. This encompasses the full spectrum of
interactions, including inbound data coming into Tracardi from various sources and outbound data being sent from
Tracardi to external systems or services.

#### Examples of Traffic:

1. **Inbound Traffic**:
    - **Event Data**: When a user performs actions on a website, such as clicking a button, submitting a form, or
      viewing a page, these interactions generate events. These events are sent to Tracardi as part of the inbound
      traffic.
    - **Webhook Data**: Data received from webhooks, such as notifications from third-party services like payment
      gateways, email marketing platforms, or CRM systems.

2. **Outbound Traffic**:
    - **API Request**: Tracardi sending data to external systems through API. This could include
      profile updates, events, etc.
    - **Integrations**: Data sent to integrated services, such as sending customer data to a marketing automation
      platform or synchronizing profiles with a CRM system.
    - **Notifications**: Sending alerts or messages to other systems or services, such as triggering an email or SMS
      notification based on specific events or conditions.

#### Example Scenario:

- **Inbound Traffic**:
    - A user visits an online store and adds items to their cart. Each interaction, such as viewing a product, adding an
      item to the cart, and starting the checkout process, generates events that are sent to Tracardi as inbound
      traffic.
    - An external payment gateway sends a webhook notification to Tracardi when a payment is successfully processed.

- **Outbound Traffic**:
    - Tracardi processes the events and updates the user's profile with their browsing and purchase behavior. This
      updated profile data is then sent to the e-commerce platform’s CRM system.
    - Based on the purchase event, Tracardi triggers an outbound notification to the email marketing platform to send a
      purchase confirmation email to the user.
