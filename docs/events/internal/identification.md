# Event: Identification

This content describes an event called "Identification" that is used when a user sends personally identifiable
information (PII) data. The expected properties of this event are listed in a table, and auto-indexing is used to
organize the data for analysis and grouping. The table also shows which event properties will be copied to event traits.
When an event occurs, the data associated with it is automatically duplicated in certain profile properties, which are
listed in another table. Write example usage

## Expected properties.

!!! Tip

    All properties are optional. If any property is missing it will not be processed and no error will be reported.

| Name        | Expected type   | Example                                                    |
|-------------|-----------------|------------------------------------------------------------|
| coupon      | string          | 20OFFSALE                                              |
| phone       | string          | +1-555-123-4567                                         |
| id          | string          | AB123456C                                               |
| discord     | string          | username#1234                                           |
| badge       | string          | gold                                                    |
| lastname    | string          | Doe                                                     |
| passport    | string          | A1234567                                                |
| credit_card | string          | 1234-5678-9012-3456                                     |
| slack       | string          | @username                                               |
| viber       | string          | +1-555-123-4567                                         |
| signal      | string          | +1-555-123-4567                                         |
| firstname   | string          | John                                                    |
| email       | string          | john.doe@example.com                                    |
| twitter     | string          | @username                                               |
| telegram    | string          | @username                                               |
| wechat      | string          | username                                                |
| login       | string          | johndoe123                                              |
| whatsapp    | string          | +1-555-123-4567                                         |

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by
copying information from the different parts of the data and putting it into a specific format that can be used to
analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized
in order to be useful.

This table describes which event property will be copied to event traits.

| Event trait            | Event properties   |
|------------------------|--------------------|
| contact.app.email      | email              |
| contact.phone          | phone              |
| pii.firstname          | firstname          |
| pii.lastname           | lastname           |
| identifier.token       | login              |
| identifier.id          | id                 |
| identifier.passport    | passport           |
| identifier.credit_card | credit_card        |
| identifier.coupon      | coupon             |
| identifier.badge       | badge              |
| contact.app.twitter    | twitter            |
| contact.app.whatsapp   | whatsapp           |
| contact.app.discord    | discord            |
| contact.app.slack      | slack              |
| contact.app.telegram   | telegram           |
| contact.app.wechat     | wechat             |
| contact.app.viber      | viber              |
| contact.app.signal     | signal             | 

## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You
can refer to the table below for the exact mapping of which fields will be copied.

| Profile field               | Event field                   | Action                                                                   |
|-----------------------------|-------------------------------|--------------------------------------------------------------------------|
| data.pii.firstname          | traits.pii.firstname          | Data will be assigned to profile always regardless if it was set or not. |
| data.pii.lastname           | traits.pii.lastname           | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.email          | traits.contact.app.email      | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.phone          | traits.contact.phone          | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.token       | traits.identifier.token       | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.id          | traits.identifier.id          | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.passport    | traits.identifier.passport    | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.credit_card | traits.identifier.credit_card | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.coupon      | traits.identifier.coupon      | Data will be assigned to profile always regardless if it was set or not. |
| data.identifier.badge       | traits.identifier.badge       | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.twitter    | traits.contact.app.twitter    | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.whatsapp   | traits.contact.app.whatsapp   | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.discord    | traits.contact.app.discord    | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.slack      | traits.contact.app.slack      | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.telegram   | traits.contact.app.telegram   | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.wechat     | traits.contact.app.wechat     | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.viber      | traits.contact.app.viber      | Data will be assigned to profile always regardless if it was set or not. |
| data.contact.app.signal     | traits.contact.app.signal     | Data will be assigned to profile always regardless if it was set or not. |

## JSON example of event properties

```json
 {
  "type": "identification",
  "properties": {
    "email": 'john.doe@example.com',
    "firstname": 'John',
    "lastname": 'Doe',
    "phone": '123-456-7890',
    "id": '123456',
    "passport": 'ABC123',
    "credit_card": '1111222233334444',
    "coupon": 'DISCOUNT10',
    "badge": 'VIP',
    "twitter": '@johndoe',
    "whatsapp": '1234567890',
    "discord": 'johndoe#1234',
    "slack": 'johndoe',
    "telegram": '@johndoe',
    "wechat": 'johndoe123',
    "viber": '1234567890',
    "signal": '1234567890'
  }
}
```

## Tracker example

```javascript
 window.tracker.track('identification', {
  email: 'john.doe@example.com',
  firstname: 'John',
  lastname: 'Doe',
  phone: '123-456-7890',
  id: '123456',
  passport: 'ABC123',
  credit_card: '1111222233334444',
  coupon: 'DISCOUNT10',
  badge: 'VIP',
  twitter: '@johndoe',
  whatsapp: '1234567890',
  discord: 'johndoe#1234',
  slack: 'johndoe',
  telegram: '@johndoe',
  wechat: 'johndoe123',
  viber: '1234567890',
  signal: '1234567890'
});
```