# Event: Checkout Started

This event should be used when a customer initiates the checkout process.

Example usage:

* User clicks on "Checkout" button in their shopping cart
* User selects "Checkout" option after adding items to their cart
* User manually navigates to the checkout page

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name     | Expected type   | Example                                 |
|----------|-----------------|-----------------------------------------|
| coupon   | string          | "SAVE10"                                |
| value    | string          | "$100.00"                               |
| id       | string          | Checkout ID: "ch_12345"                              |
| order_id | string          | "123abc"                                |
| currency | string          | "USD"                                   |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait          | Event properties   |
|----------------------|--------------------|
| ec.checkout.id       | id                 |
| ec.order.id          | order_id           |
| ec.checkout.status   | status             |
| ec.checkout.currency | currency           |
| ec.checkout.value    | value              |
| ec.checkout.coupon   | coupon             | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example of event properties

```json
{
  "coupon": "SAVE10",
  "value": "$100.00",
  "id": "ch_12345",
  "order_id": "123abc",
  "currency": "USD"
}
```