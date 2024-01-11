# Webhook bridge

Webhook bridge is used to collect unstructured data iva API call from external system. It should be used to collect data
from systems that we do not have control over the data structure that is sent. If you can structure the payload an api
call then it is better to use REST API Bridge.

Event payload is sent as unstructued data in JSON. Url defines the event and event source id.

Event properties should be send in the body of request or as URL parameters and event-type inside URL should be replaced
with the event type you would like to emit.

Tracking events with webhook

A webhook is a way for an application to provide other applications with real-time information.
It allows one application to send a message or information to another application when a specific event or trigger
occurs.

# Webhook Bridge Documentation

## Overview

### What is a Webhook Bridge?

A Webhook Bridge is a tool designed to collect unstructured data via an API call from external systems. It is
particularly useful for retrieving data from systems where the data structure is beyond our control. For structured
payloads, a REST API Bridge is recommended.

### Key Features

- Handles unstructured data in JSON format.
- Utilizes URLs to define the event and its source ID.
- Allows sending event properties in the request body or as URL parameters.
- Collect 'profile-less' events the can be matched to existing profiles.

## Tracking Events with Webhook

### Definition and Use

- Webhooks provide real-time data transmission between applications when triggered by specific events.
- Commonly used in various applications and services like social media, payment gateways, and CRM systems.

### Profile-less Events

- Profile-less events do not create a profile.
- The event enters the workflow without a profile.
- Can be matched to existing profile if there is a Profile ID, email, or phone in webhook payload.

#### Posting Profile-less Events

- Use the format: `POST /collect/EVENT-TYPE/SOURCE-ID`
- `EVENT-TYPE`: Type of the event (e.g., `coupon-received`).
- `SOURCE-ID`: ID of the event source.
- Send a JSON object in the body, which becomes the event's properties.

## Matching Profiles to Sent Data

### Process Overview

- Webhook data, while initially profile-less, can be matched against existing profiles.
- Payload must include a profile ID or an identifier (e.g., email) for matching.
- Enable profile and session creation settings for the webhook data.

### Matching Methods in Webhook Bridge

The Webhook Bridge offers two distinct methods for matching profiles based on the data available in the payload.

#### Method 1: Direct Profile ID Matching
- **Applicability**: When the payload contains a profile ID. Configure the Webhook Bridge to use this ID for loading profiles in Tracardi.
- **Operational Process**: If the ID exists in the system, the corresponding profile is matched directly.

#### Method 2: Matching via Auto Profile Merging

This method only works when system is configured to use AUTO PROFILE MERGING.

To enable this feature do the following:

  - Set the environment parameter `AUTO_PROFILE_MERGING` to a key of at least 20 characters when system starts (add it to docker command when you start tracardi API). It will be used to hash the e-mails and phones.
  - Enabling this parameter automatically activates the feature to generate and store unique IDs for every email sent to the system.
  - Generated IDs are stored in the 'profile IDS' field.
  - Email-based IDs receive prefixes like 'emm-', 'emb-', 'emp-' for main, business, and private emails, respectively.
  - Phone-based IDs use prefixes such as 'pho-', 'phm-', 'phw-', 'phb-' for mobile, main, WhatsApp, and business phones, respectively.

- **Applicability**: When a unique matching key (e.g., email or phone) is available.
- **Operational Process**:
  - Once the IDs are stored and the Webhook Bridge is set to use email or phone as an identifier, the system computes the respective ID.
  - This computed ID is then used to load profile data when an event is collected.

#### Webhook bridge configuration

To enable profile matching create an Event Source using Webhook bridge and fill the form in the following way:

1. **Create Profile and Session for Collected Data:**
    - Boolean switch to decide whether to generate a profile and session ID for webhook events.
    - Options: On (Yes) or Off (No). Select (Yes)

2. **Identification Method:**
    - Functional only when 'Create profile and session for collected data' is enabled.
    - Choose a method for profile identification: 'e-mail', 'phone', 'Custom ID', or 'none'.
    - Determines how the profile will be identified. Select 'Custom ID' for the 1st method. Select 'e-mail', 'phone' for the 2nd method.

3. **Set Profile ID from Payload:**
    - Functional only when 'Create profile and session for collected data' is enabled and Identification Method is not none.
    - Specify the location of the Profile ID Identifier in the payload.
    - Adjusts based on the chosen identification method. Reference either ID or 'e-mail', or 'phone'. 

4. **Set Session ID from Payload:**
    - Functional only when 'Create profile and session for collected data' is enabled.
    - Option to set the Session ID from the payload.
    - Specify the reference to the Session ID in the webhook payload.