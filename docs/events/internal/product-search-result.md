# Event: Product Search Result

This event should be used when a customer views a list of products or a product category as part of a search result.

For example, a customer enters a search query and clicks the "Search" button. The search results page displays a list of
products based on the customer's query, and this event is triggered when the customer views the list of products.
Example Usage

* A customer enters "shoes" in the search box and clicks "Search". The search results page displays a list of shoes, and
  the following information is captured by the event:

###Properties

* sorting: The sorting order of the products in the list. This is an array of objects, where each object contains the
  sorting key (e.g. "price") and the sorting order (e.g. "asc").
* products: An array of objects, where each object represents a product in the list. Each object contains the product
  ID, SKU, name, category, image URL, page URL, and price.
* query: The search query entered by the customer.
* filters: The filters applied by the customer to narrow down the search results. This is an array of objects, where
  each object contains the filter key (e.g. "color") and the filter value (e.g. "blue").
* type: This is always "product".

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name     | Expected type                                                                                                                         | Example                                                        |
|----------|---------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| sorting  | [{'key': 'string', 'order': 'string'}]                                                                                                | %%Write example of sorting for product-search-result event.%%  |
| products | [{'id': 'string', 'sku': 'string', 'name': 'string', 'category': 'string', 'url': {'image': 'url', 'page': 'url'}, 'price': 'float'}] | %%Write example of products for product-search-result event.%% |
| query    | string                                                                                                                                | %%Write example of query for product-search-result event.%%    |
| filters  | [{'key': 'string', 'value': 'string'}]                                                                                                | %%Write example of filters for product-search-result event.%%  |
| type     | product                                                                                                                               | %%Write example of type for product-search-result event.%%     |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait   | Event properties   |
|---------------|--------------------|
| query.type    | type               |
| query.name    | query              | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "product-search-result",
  "properties": {
    "sorting": [
      {
        "key": "price",
        "order": "asc"
      }
    ],
    "products": [
      {
        "id": "789",
        "sku": "SH001",
        "name": "Men's Running Shoes",
        "category": "Shoes",
        "url": {
          "image": "https://example.com/images/shoes1.jpg",
          "page": "https://example.com/products/sh001"
        },
        "price": 99.99
      },
      {
        "id": "790",
        "sku": "SH002",
        "name": "Women's Running Shoes",
        "category": "Shoes",
        "url": {
          "image": "https://example.com/images/shoes2.jpg",
          "page": "https://example.com/products/sh002"
        },
        "price": 89.99
      }
    ],
    "query": "shoes",
    "filters": [
      {
        "key": "color",
        "value": "blue"
      }
    ],
    "type": "product"
  }
}
```

## Tracker example

```javascript
{
  window.tracker.track("product-search-result", {
    "sorting": [
      {
        "key": "price",
        "order": "asc"
      }
    ],
    "products": [
      {
        "id": "789",
        "sku": "SH001",
        "name": "Men's Running Shoes",
        "category": "Shoes",
        "url": {
          "image": "https://example.com/images/shoes1.jpg",
          "page": "https://example.com/products/sh001"
        },
        "price": 99.99
      },
      {
        "id": "790",
        "sku": "SH002",
        "name": "Women's Running Shoes",
        "category": "Shoes",
        "url": {
          "image": "https://example.com/images/shoes2.jpg",
          "page": "https://example.com/products/sh002"
        },
        "price": 89.99
      }
    ],
    "query": "shoes",
    "filters": [
      {
        "key": "color",
        "value": "blue"
      }
    ],
    "type": "product"
  }
);
```
    