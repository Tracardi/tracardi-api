# Event: Delivery Info Entered

This event should be used when the customer adds delivery information.

## Expected properties

!!! Tip

    All properties are optional. If any property is missing, it will not be processed and no error will be reported.

| Name              | Expected type | Example                                                        |
| ----------------- | ------------ | -------------------------------------------------------------- |
| receiver          | string       | John Doe                                                       |
| delivery.postcode | string       | 12345                                                          |
| order_id          | string       | 54321                                                          |
| delivery.county   | string       | Los Angeles County                                             |
| delivery.street   | string       | 123 Main Street                                                |
| method            | string       | Standard Shipping                                              |
| delivery.country  | string       | United States                                                  |
| delivery.town     | string       | Los Angeles                                                    |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait              | Event properties |
| ------------------------ | ---------------- |
| ec.order.id              | order_id         |
| payment.method           | method           |
| ec.order.receiver        | receiver         |
| contact.address.town     | delivery.town    |
| contact.address.county   | delivery.county  |
| contact.address.country  | delivery.country |
| contact.address.postcode | delivery.postcode|
| contact.address.street   | delivery.street  |

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field                 | Event field                     | Action                                                                   |
| ----------------------------- | ------------------------------- | ------------------------------------------------------------------------ |
| data.contact.address.town     | delivery.town                    | Data will be assigned to the profile always, regardless if it was set or not. |
| data.contact.address.county   | delivery.county                  | Data will be assigned to the profile always, regardless if it was set or not. |
| data.contact.address.country  | delivery.country                 | Data will be assigned to the profile always, regardless if it was set or not. |
| data.contact.address.postcode | delivery.postcode                | Data will be assigned to the profile always, regardless if it was set or not. |
| data.contact.address.street   | delivery.street                  | Data will be assigned to the profile always, regardless if it was set or not. |

## JSON example

```json
{
  "type": "delivery-info-entered",
  "properties": {
    "receiver": "John Doe",
    "delivery": {
      "postcode": "12345",
      "county": "Los Angeles County",
      "street": "123 Main Street",
      "country": "United States",
      "town": "Los Angeles"
    },
    "order_id": "54321",
    "method": "Standard Shipping"
  }
}

```
