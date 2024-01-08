# What is Tracardi Flusher?

In the context of Tracardi, a "Flusher" is a component or worker responsible for persisting data changes to Apache
Pulsar topics. It plays a crucial role in managing data updates and ensuring that these changes are properly recorded
and stored.

Specifically, the Flusher worker collects updates or changes to data, such as profile updates, and holds these changes
in memory. It doesn't immediately write them to a database but instead buffers them for a certain period or until a
specified condition is met. This approach is often used to optimize data storage and minimize the number of database
writes.

After accumulating a set of changes or when a predefined interval or condition is met, the Flusher worker then "flushes"
or writes these changes to the appropriate data storage, such as a database. This batching of changes helps reduce the
overhead of frequent database writes, resulting in more efficient and optimized data storage operations.

The Flusher worker is particularly important in scenarios where there are many frequent updates to data, and it helps
manage and streamline the process of persisting those updates in a way that is both efficient and practical for the
system.