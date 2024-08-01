# How to send my own profile ID and disable profile ID regeneration?

To make Tracardi create a profile with a specific ID that you send, you need to enable static profile ID handling in
your event source configuration and ensure that the profile ID is included in your event data. Here's a step-by-step
guide on how to achieve this:

### Step 1: Enable Static Profile ID in Event Source

First, you need to configure the event source to allow static profile IDs. This setting ensures that Tracardi will use
the profile ID you provide rather than generating a new one.

1. **Go to Event Sources:**
    - In the Tracardi dashboard, navigate to the "Inbound Traffic" section and select "Event Sources."

2. **Edit Event Source:**
    - Find and edit the event source you are using to collect the data.

3. **Enable Static Profile ID:**
    - In the event source configuration, ensure there is an option for allowing static profile IDs. This might be a
      checkbox or a specific setting in the configuration JSON. Enable this option.

### Step 2: Include Profile ID in the Event Data

When sending events to Tracardi, include the profile ID in your tracker payload. 

```json
POST /track HTTP/1.1
Host: your-tracardi-url
Content-Type: application/json
{
"source": {
  "id": "<your-event-source-id>"
},
"profile": {
  "id": "specific-profile-id"
},
"events": [
    {
    "type": "purchase-order",
    "properties": {
        "product": "Sun glasses",
        "price": 13.45
        }
    }
]
}
```

Replace `<your-event-source-id>` and `"specific-profile-id"` with your actual event source ID and desired profile ID.
This ensures Tracardi uses the specified profile ID when processing the event.