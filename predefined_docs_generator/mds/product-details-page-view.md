# Event: Product Details Page View

The "Product Details Page View" event should be used when a customer views a product details page on an e-commerce
website. This event can be used to track customer behavior and preferences, as well as to optimize product offerings and
improve the customer experience.

Example usage:

* A customer visits the product details page for a pair of shoes on an e-commerce website. The "Product Details Page
  View" event is triggered, providing data about the product the customer viewed.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name          | Expected type   | Example                                                                 |
|---------------|-----------------|-------------------------------------------------------------------------|
| price         | float           | 49.99         |
| quantity      | int             | 1     |
| sku           | string          | SH1234           |
| id            | string          | Product ID: 123456789        |
| name          | string          | "Men's Running Shoes"        |
| url.page      | url             |"https://www.example.com/products/shoes"     |
| url.image     | url             |    "https://www.example.com/images/shoes.jpg"  |
| brand         | string          | "Nike"      |
| variant.color | string          | "black"|
| variant.size  | string          |    "9.5" |
| variant.name  | string          | "Air Max"  |
| category      | string          | "Footwear"     |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait      | Event properties   |
|------------------|--------------------|
| product.id       | id                 |
| product.name     | name               |
| product.sku      | sku                |
| product.category | category           |
| product.brand    | brand              |
| product.variant  | variant            |
| product.price    | price              |
| product.quantity | quantity           | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "product-details-page-view",
  "properties": {
    "price": 25.99,
    "quantity": 1,
    "sku": "ABC123",
    "id": "PROD001",
    "name": "Men's Running Shoes",
    "url": {
      "page": "https://www.example.com/products/mens-running-shoes",
      "image": "https://www.example.com/images/products/mens-running-shoes"
    },
    "brand": "Nike",
    "variant": {
      "color": "Blue",
      "size": "9",
      "name": "Nike Men's Running Shoes - Blue - Size 9"
    },
    "category": "Shoes/Sneakers/Men's Running Shoes"
  }
}
```

## Tracker example

```javascript
window.tracker.track("product-details-page-view", {
        "price": 25.99,
        "quantity": 1,
        "sku": "ABC123",
        "id": "PROD001",
        "name": "Men's Running Shoes",
        "url": {
            "page": "https://www.example.com/products/mens-running-shoes",
            "image": "https://www.example.com/images/products/mens-running-shoes"
        },
        "brand": "Nike",
        "variant": {
            "color": "Blue",
            "size": "9",
            "name": "Nike Men's Running Shoes - Blue - Size 9"
        },
        "category": "Shoes/Sneakers/Men's Running Shoes"
    });
```