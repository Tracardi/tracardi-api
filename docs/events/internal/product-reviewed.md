# Event: Product Reviewed 

This event should be used when a customer provides a review of a product. The review can contain feedback, comments, or suggestions regarding the product. The event can be used to analyze customer satisfaction and improve the product.

Example Usage

* A customer has written a review for a product they recently purchased.

## Expected properties. 

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.
    
| Name   | Expected type   | Example                                                 |
|--------|-----------------|---------------------------------------------------------|
| review | string          | "This product exceeded my expectations." |
| rate   | integer         | 4  |
| id     | string          | Product ID: "1234-5678"    |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by copying information from the different parts of the data and putting it into a specific format that can be used to analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait    | Event properties   |
|----------------|--------------------|
| ec.product.id     | id                 |
| ec.product.review | review             |
| ec.product.rate   | rate               | 


## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
    "type": "product-reviewed",
    "properties": {
        "review": "This product exceeded my expectations.",
        "rate": 4,
        "id": "1234-5678"
    }
}

```
    