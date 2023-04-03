# Event: Loyalty Card Added

This event should be used when a customer adds or receives a loyalty card. An example usage of this event would be when
a customer signs up for a loyalty program and is issued a loyalty card.

## Expected properties

!!! Tip All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name    | Expected type   | Example                                            |
|---------|-----------------|----------------------------------------------------|
| expires | datetime        | 2023-12-31T23:59:59.999Z                          |
| name    | string          | My Loyalty Card                                    |
| issuer  | string          | MyStore                                            |
| id      | string          | 12345                                              |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait          | Event properties   |
|----------------------|--------------------|
| loyalty.card.id      | id                 |
| loyalty.card.name    | name               |
| loyalty.card.issuer  | issuer             |
| loyalty.card.expires | expires            | 

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field             | Event field                 | Action                                                                   |
|---------------------------|-----------------------------|--------------------------------------------------------------------------|
| data.loyalty.card.id      | traits.loyalty.card.id      | Data will be assigned to profile always regardless if it was set or not. |
| data.loyalty.card.name    | traits.loyalty.card.name    | Data will be assigned to profile always regardless if it was set or not. |
| data.loyalty.card.issuer  | traits.loyalty.card.issuer  | Data will be assigned to profile always regardless if it was set or not. |
| data.loyalty.card.expires | traits.loyalty.card.expires | Data will be assigned to profile always regardless if it was set or not. |

## JSON example

Here is an example of how the event data might look in JSON format:

```json
{
  "type": "loyalty-card-added",
  "properties": {
    "expires": "2023-12-31T23:59:59.999Z",
    "name": "My Loyalty Card",
    "issuer": "MyStore",
    "id": "12345"
  }
}
