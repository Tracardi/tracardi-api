# Scaling Commercial Tracardi

Scaling Tracardi involves three main aspects: Data Bulking, Tracardi Scaling, and Infrastructure Scaling. Understanding
how Tracardi is built is essential for effectively scaling it. Tracardi ingests data through API calls, so the more data
you send, the more it can process in one run.

## Data Bulking

Tracardi allows multiple events to be sent per profile in one API call. This helps in optimizing the data ingestion
process. If you gather events for one profile, you can send them in one API call. Tracardi's JavaScript library, by
default, bulks the events registered on one page.

### How to Send Bulk Events

Tracardi's API schema supports sending multiple events for one profile. Here is an example of an API bulk payload:

```json
{
  "source": {
    "id": "Source ID"
  },
  "session": {
    "id": "Session ID"
  },
  "profile": {
    "id": "Profile ID"
  },
  "events": [
    {
      "type": "event-type",
      "properties": {
        // Event properties
      }
    },
    // Multiple events for one profile
    ...
  ]
}
```

## Tracardi Scaling

!!! Note

    Scaling may require several rounds of system adjustments. Please thoroughly test the configurations before going live. 

### API Scaling

Each API call takes time to process, so a single API instance has a limited number of calls it can handle. To handle
more API calls, replicate the `tracardi-api` Docker container. Starting with at least 10 replicas is a good approach.
The API sends data to Apache Pulsar, which is then consumed by background workers.

```yaml title="Example of Helm Chart values file. Param replicas will scale the number of private/public API" linenums="1" hl_lines="7"
# API configuration
api:
  private:
    replicas: 1  # Number of replicas for the private API

  public:
    replicas: 1  # Number of replicas for the public API (This is the API you need to scale for consumption) 
```

### Scaling Background Workers

To process data quickly, scale the number of background workers. Ensure there are enough workers to process data so that
no data is left in the Apache Pulsar topic. Depending on the number of bulked events, you may need different numbers of
background worker replicas.

```yaml title="Example of Helm Chart values file. Param replicas will scale the number of worker" linenums="1" hl_lines="4"
# Worker configuration
worker:
  background:
    replicas: 1  # Number of replicas for the background worker
```

Run a test and monitor the backlog of Apache Pulsar via the Tracardi API using the `/queue/{namespace}/{topic}/backlog`
endpoint. This will tell you how quickly the data is consumed. The namespace and topic you want to monitor are `system`
and `functions`, respectively. The response will look something like this:

```json
{
  "total": 0,
  "backlog": [
    {
      "partition": "persistent://tracardi/system/functions-partition-0",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-2",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    ...
  ]
}
```

Ensure the `count` on each partition is low or equal to 0. This number tells how many messages are not consumed. Near
realtime consumption will keep this number low.

## Infrastructure Scaling

### Apache Pulsar

Begin by scaling Pulsar. Refer to Apache Pulsar documentation for detailed scaling instructions.

To scale Apache Pulsar, you need to focus on scaling its main components: brokers, bookies, and ZooKeeper nodes. Brokers
handle client connections and manage topic partitions, so increasing the number of brokers improves load distribution
and fault tolerance. Bookies store message data, so adding more bookies enhances storage capacity and write/read
throughput. ZooKeeper nodes manage metadata and coordination; scaling them ensures higher availability and resilience of
the cluster. Properly balancing and scaling these components ensures Apache Pulsar can efficiently handle increased
traffic and data loads.

### Elasticsearch

By default, Tracardi saves events in bulks to Elasticsearch with a bulk size of 500 events. Monitor if the background
workers are filling
the predefined bulk size or if they trigger saving due to buffer timeout. Tracardi will save 500 events at once if they
arrive within a specific timeframe (e.g., 30 seconds). If not, the buffer will be emptied, and only the collected events
will be saved.

To ensure Elasticsearch can handle the data, define the number of nodes and the number of shards for the event index.
Changing the number of shards post-setup is not possible. When installing Tracardi use environment variables to
configure at least
one data replica and set up shards for each index. Look for `ELASTIC_INDEX_REPLICAS` and `ELASTIC_INDEX_SHARDS`.

Proper scaling ensures that Tracardi can efficiently handle large volumes of data, providing a robust solution for
commercial needs.

## Production installation check-list

Deploying a production environment of Tracardi requires careful planning and optimization to ensure that the system is
efficient, scalable, and reliable. This article provides recommendations for deploying Tracardi in a production setting,
covering key considerations to help you achieve an optimal setup.

### 1. Initial Production Setup Is Not Final

The first deployment of Tracardi in a production environment should be seen as a starting point rather than a final
setup. It's crucial to continuously measure and tweak performance based on Key Performance Indicators (KPIs). This
iterative process helps in identifying optimization opportunities in various components as discussed below.

### 2. Event Consumption

Understanding the volume of events your system will consume is foundational. The database, Tracardi's interaction with
Apache Pulsar, API replicas, and worker configurations must all be adjusted based on the peak performance requirements.
Start by establishing the maximum number of events you expect to process.

### 3. ElasticSearch Configuration

ElasticSearch plays a critical role in Tracardi's performance. Deciding on the number of nodes, shards per index, and
data replicas is essential. Remember, altering the number of shards post-setup can be challenging. Utilize Tracardi
environment variables to configure at least one data replica and set up shards for each index. Please look
for `ELASTIC_INDEX_REPLICAS`, and `ELASTIC_INDEX_SHARDS`.

### 4. Data Backup

For ElasticSearch data, using S3 storage for backups is recommended. This should be defined during the ElasticSearch
installation process to ensure data durability and availability. Please see Elasticsearch documentation for backup
settings.

### 5. Data Partitioning

Data partitioning is a critical strategy for managing large datasets. It involves dividing a database into distinct,
parts to improve manageability, performance, and availability. Please see
this [documentation on data partitioning](data_partitioning.md).

### 5. Data Retention in ElasticSearch

Determine how long data should reside on hot nodes, considering that ElasticSearch doesn't define cold nodes by default.
Plan the transition of data from hot to warm and cold nodes, setting up a comprehensive data retention policy within
ElasticSearch. Please see Elasticsearch documentation for nodes settings.

### 6. Apache Pulsar Data Policy

Like ElasticSearch, Apache Pulsar requires a data retention policy that specifies the duration data is stored and the
offloading process when data is no longer needed. S3 storage is a good option for offloading, with considerations for
data deletion over time. Default retention policy is set to 30 days and 1GB of storage.

### 7. Apache Pulsar Configuration

Based on your traffic, decide on the number of brokers and bookies needed to handle the load efficiently. Regularly
monitor Apache Pulsar's performance against your traffic to ensure it meets your requirements.

### 8. Tracardi API and Storage Workers

Optimize the number of Tracardi API and storage workers based on your workload. These configurations directly impact
data processing and storage efficiency.

### 9. Cache and Database Connections

Adjust cache times and MySQL connection pools as needed. For instance, modifying the `MYSQL_CONNECTION__POOL` variable
and increasing MySQL connections can help manage load. Balancing API connections and cache TTLs can optimize
performance.

### 10. Distributed Cache Configuration

Ensure your Redis distributed cache has sufficient memory to handle the anticipated load. Testing with an estimated
number of user profiles can help determine the required memory capacity.

### 11. Storage Workers Settings

Define the optimal number of storage workers, which bulk and batch data for storage. The default setting is 500 records
per batch, but this may need adjustment based on your specific needs.

### 12. Logging Level

Set the logging level to "warning" by default to minimize data overhead. Detailed logging can significantly increase
data volume and should be used selectively during system tuning phases. Please see `LOGGING_LEVEL` env variable.

### 13. Security

Set the `AUTO_PROFILE_MERGING` and `INSTALLATION_TOKEN` to your custom values.

### Conclusion

Deploying Tracardi in a production environment requires a detailed understanding of your performance needs and careful
configuration of various components. By following these recommendations, you can create a robust and scalable system
capable of handling your event processing and data management requirements efficiently. Continuously monitor and adjust
your setup to ensure optimal performance as your needs evolve.