# What is the difference between event traits and properties and what is event indexing?

Event traits and properties are both characteristics of an event in Tracardi, but they differ in their structure and
purpose.

Event properties are the basic characteristics of an event that can be recorded and searched, but they cannot be
directly aggregated. Properties have the characteristic of being able to save any data, even if there is a collision in
data type. A collision in data types occurs when the data is sent as a number in one instance and as a string in another
instance. For example, "Age" can be sent as the number 24 or the string "24 years old." Properties are able to store
this data even if it is inconsistent or has different data types.

Event traits, on the other hand, are structured and have data types. Event traits are used for searching, analyzing, and
aggregating events. If the data is inconsistent or has an incorrect data type, such as having "Age" as a number but
receiving it as a string ("24 yeas old"), Tracardi will throw an error and not index it. Data in traits have structure and
types, allowing for aggregation, such as calculating the average age based on the "age" trait.

To summarize, if an event includes a property, that property could be copied to a trait so that all events involving
this attribute could be identified and aggregated. Copied property gets removed from properties, and it is moved to traits. 
Properties allow for recording and searching, while traits enable analysis and aggregation with structured indexing.
Not all data must be moved from properties to traits only the one you think you will need to aggregate the events.

---
This document answers the following questions:
- What is event indexing?
- What is event indexing used for?
- How can I aggregate data in events?
- Why I can not aggregate data in events?