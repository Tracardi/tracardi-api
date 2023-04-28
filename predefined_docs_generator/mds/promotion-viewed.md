# Event: Promotion Viewed

This event should be used when a customer viewed a promotion banner or text.

Example Usage

* A customer visits a website and sees a promotion banner on the homepage. They don't click on it but continue browsing
  the site.

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name        | Expected type   | Example                                                      |
|-------------|-----------------|--------------------------------------------------------------|
| id          | string          | 123456          |
| name        | string          | "Promo Banner"        |
| media.image | string          | "http://web.com/banner.jpg" |
| media.text  | string          | "Visit my page"  |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait    | Event properties   |
|----------------|--------------------|
| promotion.id   | id                 |
| promotion.name | name               | 

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "promotion_viewed",
  "properties": {
    "media": {
      "text": "50% off on all products",
      "image": "https://example.com/promotion_banner.jpg"
    },
    "name": "April Promotion",
    "id": "123456"
  }
}

```
    