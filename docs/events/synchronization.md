# Events synchronization

Profile synchronization is an important aspect of data management, particularly when working with customer data platforms or other systems that process large volumes of events and actions related to individual profiles. By coordinating the processing of events and actions, organizations can ensure that data is accurate, consistent, and up-to-date, and that actions and processes are performed in the correct order. 

Here is an example of how profile synchronization might be used in a customer data platform:

Imagine that an online retailer tracks events related to customer profiles, such as product searches, purchases, and customer service interactions. Tracardi might receive many events each second, including events related to different customer profiles.

To ensure that events are processed accurately and consistently, Tracardi implements profile synchronization. This makes processing events for each customer profile sequentially, so that events related to one customer are fully processed one by one even if they are send at the same time. This ensures that the data for each customer is accurate and up-to-date, and that actions and processes are performed in the correct order.

For example: If you want to send two messages and the second message depends on the result of the first one, the system must wait for the first event to be finished before sending the second message.

Without profile synchronization, it is possible that events for different customer profiles could be processed out of order, leading to inconsistencies and errors in the data.
