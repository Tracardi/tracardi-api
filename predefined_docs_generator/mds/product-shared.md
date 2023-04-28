# Event: Product Shared

This event should be used when a customer shares a product with others, for example by sending a link to the product
page via email or social media. It can provide valuable insights into how customers are engaging with your products and
can help you identify which products are being shared the most.

Example usage:

* A customer is browsing your website and finds a product they really like. They click on the "Share" button and choose
  to send a link to the product page to a friend via email. This action would trigger the "Product Shared" event.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name   | Expected type   | Example                                              |
|--------|-----------------|------------------------------------------------------|
| media  | string          | "Facebook" |
| id     | string          | Product ID: "abc-1234"    |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

Data will not be indexed.

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "product-shared",
  "properties": {
    "media": "Facebook",
    "id": "abc-1234"
  }
}

```
    