# Event: Search 

This event should be used when a customer searches a website or app.

## Expected properties. 

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.
    
| Name     | Expected type   | Example                                         |
|----------|-----------------|-------------------------------------------------|
| query    | string          | "Contact page"    |
| category | string          | "Search" |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by copying information from the different parts of the data and putting it into a specific format that can be used to analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait              | Event properties   |
|--------------------------|--------------------|
| hit.page.search.category | category           |
| hit.page.search.query    | query              | 


## Copy event data to profile

Data will not be copied to profile.

## JSON example

```json
{
  "type": "Search",
  "properties": {
    "query": "Contact email",
    "category": "Search"
  }
}
```


    