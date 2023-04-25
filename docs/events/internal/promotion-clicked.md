# Event: Promotion Clicked

This event should be used when a customer clicks on a promotion banner, such as a banner ad or pop-up window.

## Expected properties.

!!! Tip 

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

Name    | Expected Type    |Description
--------|---------------|-------------------
id    |String    | A unique identifier for the promotion (e.g. promo123).
name|    String    |The name or title of the promotion.
url.image |    URL |    The URL of the promotion image/banner.
url.page    |URL    |The URL of the promotion landing page.

## Auto indexing

Data will not be indexed.

## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "event": "promotion-clicked",
  "properties": {
    "id": "promo123",
    "name": "Summer Sale",
    "url": {
      "image": "https://example.com/promo123.jpg",
      "page": "https://example.com/promo123"
    }
  }
}

```
    