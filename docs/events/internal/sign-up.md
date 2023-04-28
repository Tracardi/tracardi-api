# Event: Sign-Up

When a user signs up for a service, this event should be used to track it. This could also be an identification point
for profile merging.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name      | Expected type   | Example                                           |
|-----------|-----------------|---------------------------------------------------|
| lastname  | string          | "John" |
| firstname | string          | "Doe" |
| email     | string          |"johndoe@example.com"     |
| login     | string          | "johndoe@example.com"    |
| custom    | object          | Any additional data like: plan, tier, etc. {"plan": "premium"}   |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait      | Event properties   |
|------------------|--------------------|
| contact.app.email    | email              |
| pii.firstname    | firstname          |
| pii.lastname     | lastname           |
| identifier.token | login              | 

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field         | Event field             | Action                                                                   |
|-----------------------|-------------------------|--------------------------------------------------------------------------|
| data.contact.email    | traits.contact.app.email    | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.token | traits.identifier.token | Data will be assigned to profile always regardless if it was set or not. |
| data.pii.firstname    | traits.pii.firstname    | Data will be assigned to profile always regardless if it was set or not. |
| data.pii.lastname     | traits.pii.lastname     | Data will be assigned to profile always regardless if it was set or not. |

## JSON example

```json
{
  "type": "sign-up",
  "properties": {
    "lastname": "Doe",
    "firstname": "John",
    "email": "johndoe@example.com",
    "login": "johndoe",
    "custom": {
      "plan": "premium",
      "source": "google",
      "campaign": "spring_sale"
    }
  }
}

```

## Tracker example

```javascript
window.tracker.track("sign-up", {
        "lastname": "Doe",
        "firstname": "John",
        "email": "johndoe@example.com",
        "login": "johndoe",
        "custom": {
            "plan": "premium",
            "source": "google",
            "campaign": "spring_sale"
        }
    }
);

```
    