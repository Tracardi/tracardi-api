# Event: Checkout Status

This event should be used when a customer completes a checkout step and the status changes. An example usage of this
event is when a customer has completed the payment process and the status of the checkout changes from "pending" to "
paid".

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                                |
|--------|-----------------|--------------------------------------------------------|
| status | string          | "paid" |
| id     | string          | Checkout ID: "ch_123abc456def"     |

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

Data will not be copied to profile.

## JSON example of event properties

```json
{
  "type": "checkout-status",
  "properties": {
    "status": "paid",
    "id": "ch_123abc456def"
  }
}
```


    