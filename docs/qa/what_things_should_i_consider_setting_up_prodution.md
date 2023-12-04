# What should I pay attention to when setting up production ready Tracardi.

When setting up Tracardi for production, it's crucial to consider several factors that can impact its performance and
efficiency. These factors include:

1. **Event Volume and Traffic Spikes:**
   Analyze the anticipated event volume and potential traffic spikes to determine if Tracardi should be deployed behind
   a queue. Queues effectively manage surges in traffic, ensuring smooth event processing and preventing system
   overload.

2. **Event Payload Size:**
   Assess the average size of event payloads. Larger payloads require more resources and may result in slower processing
   compared to smaller events. Optimize event payloads by eliminating unnecessary data to enhance performance.

3. **Event Storage and Retention:**
   Consider the number of events stored per day and its impact on other processes, such as segmentation. Determine the
   desired data retention period, as longer retention increases query size and segmentation complexity.

4. **Index Granularity and Data Partitioning:**
   Decide how to partition event data into indices. Default quarterly indices create four indices per year, while
   monthly splits require more indices and may impact query performance. Monthly splits offer more granular data storage
   and archiving.

5. **Customer Volume and Segmentation:**
   Evaluate the number of customers that Tracardi will handle. Customer volume can affect segmentation performance.
   Elasticsearch excels at data aggregation, but storing profile data can be time-consuming.

By carefully considering these factors, you can optimize Tracardi's performance and ensure it meets your production
requirements.