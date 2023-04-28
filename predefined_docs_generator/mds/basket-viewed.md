# Event: Basket Viewed 

This event should be used when a customer has viewed their shopping cart. An example usage would be when a user logs into their account and clicks on the shopping cart icon to view the items in their cart.

## Expected properties

!!! Tip
    
    All properties are optional. If any property is missing it will not be processed and no error will be reported.
    
| Name   | Expected type   | Example                                          |
|--------|-----------------|--------------------------------------------------|
| id     | string          | Basket ID: "1234-abcd-5678-efgh"                             |

## Auto indexing

Auto indexing is not applicable for this event.

## Copy event data to profile

Data will not be copied to profile for this event.

## JSON example

```json
{
  "event": "basket-viewed",
  "properties": {
    "id": "1234-abcd-5678-efgh"
  }
}
```