# Event: Product Clicked

This event is typically triggered when a customer clicks on a specific product on a website or mobile app. The expected
properties for this event include information such as the product price, quantity, SKU, ID, position on the page, name,
URL, brand, variant information, and category. All of these properties are optional and will not cause errors if they
are not included.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name          | Expected type   | Example                                                       |
|---------------|-----------------|---------------------------------------------------------------|
| price         | float           | 19.99         |
| quantity      | int             | 1      |
| sku           | string          | "12345"         |
| id            | string          |Product ID: "12345-abc-398jsd8"            |
| position      | int             | 1     |
| name          | string          | "Example Product"          |
| brand         | string          | "Adidas"         |
| url.image     | url             | https://www.example.com/products/example-product/image.jpg     |
| url.page      | url             | https://www.example.com/products/example-product      |
| variant.size  | string          | XL  |
| variant.color | string          | "Red" |
| variant.name  | string          | "Red LS"  |
| category      | string          | "Apparel"      |

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
| product.position | position           | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "price": 19.99,
  "quantity": 1,
  "sku": "12345",
  "id": "67890",
  "position": 2,
  "name": "Example Product",
  "url": {
    "page": "https://www.example.com/products/example-product",
    "image": "https://www.example.com/products/example-product/image.jpg"
  },
  "brand": "Example Brand",
  "variant": {
    "size": "Small",
    "name": "Example Product - Small - Red",
    "color": "Red"
  },
  "category": "Example Category"
}

```

## Tracker example

```javascript
// Track Product Clicked event
window.tracker.track('product-clicked', {
    "price": 19.99,
    "quantity": 1,
    "sku": "12345",
    "id": "67890",
    "position": 2,
    "name": "Example Product",
    "url":{
        "page": "https://www.example.com/products/example-product",
        "image": "https://www.example.com/products/example-product/image.jpg"
    },
    "brand": "Example Brand",
    "variant": {
        "size": "Small",
        "name": "Example Product - Small - Red",
        "color": "Red"
    },
    "category": "Example Category"
  });


```
    