# Event: Loyalty Card Removed

This event should be used when a customer removes or deletes a loyalty card from their account. For example, when a
customer cancels a loyalty program membership or their account is terminated.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                                 |
|--------|-----------------|---------------------------------------------------------|
| id     | string          | "jsd84mj-smks8rmd-sksjd" |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait     | Event properties   |
|-----------------|--------------------|
| loyalty.card.id | id                 | 

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field             | Event field   | Action                |
|---------------------------|---------------|-----------------------|
| data.loyalty.card.id      |               | Data will be deleted. |
| data.loyalty.card.name    |               | Data will be deleted. |
| data.loyalty.card.issuer  |               | Data will be deleted. |
| data.loyalty.card.expires |               | Data will be deleted. |

## JSON example

Here is an example of how the event data might look in JSON format:

```json
{
  "type": "loyalty-card-removed",
  "properties": {
    "id": "12345"
  }
}
```
    