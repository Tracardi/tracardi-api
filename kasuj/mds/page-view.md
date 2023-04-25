# Event: Page View

This event should be used to track when a user views a page on a website or application. It can provide insights into
user behavior and preferences.

Example Usage:

A user visits a product page on an e-commerce website. The Page View event can be triggered to record the user's
interaction with the page, including the product details, images, and other related information.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name     | Expected type   | Example                                            |
|----------|-----------------|----------------------------------------------------|
| category | string          | "Contact" |

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
    