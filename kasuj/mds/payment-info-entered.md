# Event: Payment Info Entered

This event should be used when a customer adds payment information during checkout.

Example usage:

* A customer enters their credit card information on the checkout page.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name                | Expected type   | Example                                                                  |
|---------------------|-----------------|--------------------------------------------------------------------------|
| credit_card.cvv     |                 | 123    |
| order_id            | string          | "12345-abcde-67890"            |
| credit_card.expires | string          |    "02/24" |
| method              | string          | "credit_card"             |
| credit_card.holder  | string          | "John Doe" |
| credit_card.number  | string          | "4111-1111-1111-1111"  |

## Auto indexing

Data will not be indexed.

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "payment-info-entered",
  "properties": {
    "order_id": "123456",
    "method": "credit_card",
    "credit_card": {
      "holder": "John Doe",
      "number": "4111111111111111",
      "expires": "06/24",
      "cvv": "123"
    }
  }
}
```


    