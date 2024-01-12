# Adding New Default Event Types in Tracardi

## Overview

In Tracardi, default event types are essential tools for tracking user interactions and system processes. Defined in
JSON format, these event types are available immediately after system installation. They encompass a range of standard
e-commerce event types, properties, mappings, and optional code for advanced customization.

### Example of a JSON File for Default Event Types

```json
[
  {
    "name": "Product Search Result",
    "description": "Customer viewed a product list or product category.",
    "id": "product-search-result",
    "properties": {
      "type": "product",
      "query": "string",
      "filters": [
        {
          "key": "string",
          "value": "string"
        }
      ],
      "sorting": [
        {
          "key": "string",
          "order": "string"
        }
      ],
      "products": [
        {
          "id": "string",
          "sku": "string",
          "name": "string",
          "category": "string",
          "url": {
            "image": "url",
            "page": "url"
          },
          "price": "float"
        }
      ]
    },
    "copy": {
      "hit.query": "properties.query"
    },
    "tags": [
      "activity:browsing",
      "activity:browsing:search",
      "event:operational"
    ],
    "state": "awareness"
  }
  // More event types...
]
```

## File Location and Structure

Default event types are defined in JSON files located in the `tracardi/service/setup/events` folder. Each file contains
a list of objects, each representing an event type. The schema for these objects includes:

1. **Type**: Unique event ID.
2. **Name**: Event type name.
3. **Description**: Details about the event and its data.
4. **Properties**: Schema of properties as a template for event properties.
5. **Copy**: Rules for copying properties within an event.
6. **Profile**: Event-to-profile mapping rules.
7. **State**: Customer journey state associated with the event.
8. **Compute**: Python code executed during the event’s consumption.

### Example

```json
{
  "name": "Message Sent",
  "description": "Message was sent to the customer.",
  "id": "message-sent",
  "properties": {
    "id": "string",
    "conversation": "string",
    "type": "online-message|newsletter|...",
    "message": "string",
    "sender": "string",
    "recipient": "string",
    "identity": {
      "phone": {
        "main": "string",
        "mobile": "string",
        "whatsapp": "string",
        "business": "string"
      },
      "email": {
        "main": "string",
        "private": "string",
        "business": "string"
      }
    }
  },
  "copy": {
    "data.contact.email.main": "properties.identity.email.main",
    "data.contact.email.private": "properties.identity.email.private",
    "data.contact.email.business": "properties.identity.email.business",
    "data.contact.phone.main": "properties.identity.phone.main",
    "data.contact.phone.mobile": "properties.identity.phone.mobile",
    "data.contact.phone.whatsapp": "properties.identity.phone.whatsapp",
    "data.contact.phone.business": "properties.identity.phone.business",
    "data.message.id": "properties.id",
    "data.message.conversation": "properties.conversation",
    "data.message.type": "properties.type",
    "data.message.text": "properties.message",
    "data.message.recipient": "properties.recipient",
    "data.message.sender": "properties.sender"
  },
  "profile": {
    "data.contact.email.main": [
      "data.contact.email.main",
      "equals_if_not_exists"
    ],
    "data.contact.email.private": [
      "data.contact.email.private",
      "equals_if_not_exists"
    ],
    "data.contact.email.business": [
      "data.contact.email.business",
      "equals_if_not_exists"
    ],
    "data.contact.phone.main": [
      "data.contact.phone.main",
      "equals_if_not_exists"
    ],
    "data.contact.phone.business": [
      "data.contact.phone.business",
      "equals_if_not_exists"
    ],
    "data.contact.phone.mobile": [
      "data.contact.phone.mobile",
      "equals_if_not_exists"
    ],
    "data.contact.phone.whatsapp": [
      "data.contact.phone.whatsapp",
      "equals_if_not_exists"
    ]
  }
},
```

Above example defines `Message Sent` event type. In properties we have default values for this event:

```
    "properties": {
      "id": "string",
      "conversation": "string",
      "type": "online-message|newsletter|...",
      "message": "string",
      "sender": "string",
      "recipient": "string",
      "identity": {
        "phone": {
          "main": "string",
          "mobile": "string",
          "whatsapp": "string",
          "business": "string"
        },
        "email": {
          "main": "string",
          "private": "string",
          "business": "string"
        }
      }
    },
```

This is a template for the event properties, only selected properties may be set. If property is not set it will not be
copied to the profile if such operation is defined.

#### Coping data within event

```
    "copy": {
      "data.contact.email.main": "properties.identity.email.main",
      "data.contact.email.private": "properties.identity.email.private",
      "data.contact.email.business": "properties.identity.email.business",
      "data.contact.phone.main": "properties.identity.phone.main",
      "data.contact.phone.mobile": "properties.identity.phone.mobile",
      "data.contact.phone.whatsapp": "properties.identity.phone.whatsapp",
      "data.contact.phone.business": "properties.identity.phone.business",
      "data.message.id": "properties.id",
      "data.message.conversation": "properties.conversation",
      "data.message.type": "properties.type",
      "data.message.text": "properties.message",
      "data.message.recipient": "properties.recipient",
      "data.message.sender": "properties.sender"
    },
```

Copy defines how data should be copied inside the event. Because properties are not indexed some of the data could be
copied to `data` key which is indexed and therefore can be searched. Key defines the destination and value defines the
source of the data.

For example __"data.contact.email.main": "properties.identity.email.main",__ means copy data
from `properties.identity.email.main` to `data.contact.email.main` or other
words `data.contact.email.main`=`properties.identity.email.main`.

#### Mapping event data to profile

```

    "profile": {
      "data.contact.email.main": [
        "data.contact.email.main",
        "equals_if_not_exists"
      ],
      "data.contact.email.private": [
        "data.contact.email.private",
        "equals_if_not_exists"
      ],
      "data.contact.email.business": [
        "data.contact.email.business",
        "equals_if_not_exists"
      ],
      "data.contact.phone.main": [
        "data.contact.phone.main",
        "equals_if_not_exists"
      ],
      "data.contact.phone.business": [
        "data.contact.phone.business",
        "equals_if_not_exists"
      ],
      "data.contact.phone.mobile": [
        "data.contact.phone.mobile",
        "equals_if_not_exists"
      ],
      "data.contact.phone.whatsapp": [
        "data.contact.phone.whatsapp",
        "equals_if_not_exists"
      ]
    }
```

Copy defines how data should be copied from event to profile. Key means the profile field. First array value is the
event field and 2nd value is the way to copy data. There are several methods of applying new data to profile:

- **equals** - overrides existing data
- **equals_if_not_exists** - keeps old data intact and only applies new data if there is no data in the profile field
- **increment** - increments value
- **decrement** - decrements value
- **delete** - deletes data (then the 1st array field should be null)

## Configuration Steps

To add a new default event type in Tracardi:

1. **Navigate**: Go to the `tracardi/service/setup/events` folder.
2. **Create/Edit**: Create or edit a JSON file within this folder.
3. **Define**: Adhere to the schema, ensuring a unique Type ID and necessary field specifications.
4. **Customize**: Optionally, add Python code in the Compute field for advanced features.
5. **Restart**: Restart the system to apply changes.

## Documentation and Maintenance

Once a new event type is defined, it is automatically documented within Tracardi. Access this documentation under the
‘Maintenance’ section, specifically in ‘Default Event Types’.
