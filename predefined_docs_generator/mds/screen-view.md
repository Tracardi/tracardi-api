# Event: Screen View

The "Screen View" event should be used to track when a customer views a screen or a page on a mobile device. This event can help to understand how customers navigate through an application or website, and identify popular or problematic screens.

Example usage:

* A customer navigates to the "Home" screen of a mobile shopping application.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name     | Expected type   | Example                                              |
|----------|-----------------|------------------------------------------------------|
| name     | string          | "Product list"    |
| category | string          | "Shopping" |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait       | Event properties   |
|-------------------|--------------------|
| hit.page.name     | name               |
| hit.page.category | category           | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "event_type": "screen-view",
  "properties": {
    "name": "Product Detail Screen",
    "category": "Product"
  }
}

```
    