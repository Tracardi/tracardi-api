# Event: Page Print

This event should be used when a customer prints a page. It can be useful to track how many users are printing pages and
which pages are being printed most frequently.

Example usage:
* A user prints a product page on an e-commerce website to show the product information to a friend.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name     | Expected type   | Example                                             |
|----------|-----------------|-----------------------------------------------------|
| category | string          | "Product Details" |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait       | Event properties   |
|-------------------|--------------------|
| hit.page.category | category           | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "page-print",
  "properties": {
    "category": "Product Details"
  }
}
```
    
    