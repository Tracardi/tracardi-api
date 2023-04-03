# Event: Checkout Completed

This event should be used when a customer has completed the check-out process. An example usage would be when a user
adds items to their cart, enters their payment and shipping information, and clicks "Submit Order."

## Expected properties

!!! Tip All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                               |
|--------|-----------------|-------------------------------------------------------|
| id     | string          | "5678-efgh-1234-abcd"                                 |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait     | Event properties   |
|-----------------|--------------------|
| checkout.id     | id                 |
| checkout.status | status             | 

## Copy event data to profile

Data will not be copied to profile for this event.

## JSON example of event properties

```json
{
  "properties": {
    "id": "5678-efgh-1234-abcd"
  }
}