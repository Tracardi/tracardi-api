# Event: Product Removed From Basket

This event should be used when a customer removes a product from their shopping cart.

Example Usage:

* A customer has added a pair of shoes to their shopping cart but decides to remove it before completing the purchase.
  The "Product Removed from Basket" event would be triggered.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.


| Name          | Expected type | Example                                        |
|---------------|---------------|------------------------------------------------|
| price         | float         | 10.99                                          |
| quantity      | int           | 2                                              |
| sku           | string        | 1234                                           |
| id            | string        | Product ID: 5678                                           |
| name          | string        | Blue T-Shirt                                   |
| url.page      | url           | "https://example.com/products/1234"            |
| url.image     | url           | "https://example.com/products/1234/image.jpg"  |
| brand         | string        | Nike                                           |
| variant.color | string        | Blue                                           |
| variant.size  | string        | Medium                                         |
| variant.name  | string        | Blue T-Shirt - Medium                          |
| category      | string        | Clothing > T-Shirts > Men's                    |


## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait      | Event properties   |
|------------------|--------------------|
| ec.product.id       | id                 |
| ec.product.name     | name               |
| ec.product.sku      | sku                |
| ec.product.category | category           |
| ec.product.brand    | brand              |
| ec.product.variant  | variant            |
| ec.product.price    | price              |
| ec.product.quantity | quantity           | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example
```json
{
  "type": "product-removed-from-basket",
  "properties": {
    "price": 19.99,
    "quantity": 2,
    "sku": "TSB001",
    "id": "12345",
    "name": "Black T-Shirt",
    "url": {
      "page": "https://example.com/products/tsb001"
    },
    "brand": "Example Brand",
    "variant": {
      "color": "Black",
      "size": "M",
      "name": "Black T-Shirt - M"
    },
    "category": "Clothing"
  }
}
```


## Tracker example

```javascript
window.tracker.track("product-removed-from-basket", {
    "price": 19.99,
    "quantity": 2,
    "sku": "TSB001",
    "id": "12345",
    "name": "Black T-Shirt",
    "url": {
      "page": "https://example.com/products/tsb001"
    },
    "brand": "Example Brand",
    "variant": {
      "color": "Black",
      "size": "M",
      "name": "Black T-Shirt - M"
    },
    "category": "Clothing"
  });
```
    