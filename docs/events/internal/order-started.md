# Event: Order Started

The Order Started event should be used to track when a customer starts an order on your website or app. This event can
help you understand how many orders are being placed and what products are being purchased.

Example usage:

* A customer places an order on an e-commerce website. The Order Started event is triggered as soon as the customer
  completes the order and stats checkout process.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name           | Expected type                                                                                                                                                                                                                                   | Example                                                      |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|
| id             | string                                                                                                                                                                                                                                          | "ORD-123456"           |
| products       | [{'id': 'string', 'name': 'string', 'sku': 'string', 'category': 'string', 'brand': 'string', 'variant': {'name': 'string', 'color': 'string', 'size': 'string'}, 'price': 'float', 'quantity': 'int', 'url': {'image': 'url', 'page': 'url'}}] | [{"id": "P12345", "name": "Product 1", "price": 19.99, "quantity": 2}, {"id": "P67890", "name": "Product 2", "price": 9.99, "quantity": 1}]      |
| affiliation    | string                                                                                                                                                                                                                                          | "google"   |
| income.revenue | float                                                                                                                                                                                                                                           | 100.0 |
| income.value   | float                                                                                                                                                                                                                                           | 95.0   |
| cost.other     | float                                                                                                                                                                                                                                           | 10.0   |
| cost.shipping  | float                                                                                                                                                                                                                                           | 5.0  |
| cost.discount  | float                                                                                                                                                                                                                                           | 5.0  |
| cost.tax       | float                                                                                                                                                                                                                                           | 9.0       |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait      | Event properties   |
|------------------|--------------------|
| ec.order.id      | id                 |
| ec.order.status  | status             | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "order-started",
  "properties": {
    "id": "order_12345",
    "products": [
      {
        "id": "product_123",
        "name": "Product 1",
        "sku": "prod1_123",
        "category": "Electronics",
        "brand": "Brand 1",
        "variant": {
          "name": "Variant 1",
          "color": "Red",
          "size": "XL"
        },
        "price": 8.99,
        "quantity": 1,
        "url": {
          "image": "https://example.com/image.jpg",
          "page": "https://example.com/product.html"
        }
      }
    ],
    "affiliation": "Google",
    "income": {
      "revenue": 8.99,
      "value": 10.00
    },
    "cost": {
      "other": 5.00,
      "discount": 2.00,
      "shipping": 3.00,
      "tax": 0.99
    }
  }
}
```
    