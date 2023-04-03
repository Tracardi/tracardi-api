# Event: Order Completed

This event should be used when a customer completes an order.

## Expected properties

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                                 |
|--------|-----------------|---------------------------------------------------------|
| id     | string          | "jsd84mj-smks8rmd-sksjd" |
| status | string          | "Completed" |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait   | Event properties   |
|---------------|--------------------|
| order.id      | id                 |
| order.status  | status             | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "order-completed",
  "properties": {
    "order": {
      "id": "12345",
      "status": "completed"
    }
  }
}
```