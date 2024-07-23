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
      },
      "options": {
        // Event options
      }
    }
    // Multiple events for one profile
  ]
}
```

## Tracardi Scaling

### API Scaling

Each API call takes time to process, so a single API instance has a limited number of calls it can handle. To handle
more API calls, replicate the `tracardi-api` Docker container. Starting with at least 10 replicas is a good approach.
The API sends data to Apache Pulsar, which is then consumed by background workers.

### Scaling Background Workers

To process data quickly, scale the number of background workers. Ensure there are enough workers to process data so that
no data is left in the Apache Pulsar topic. Depending on the number of bulked events, you may need different numbers of
background worker replicas.

Monitor the backlog of Apache Pulsar via the Tracardi API using the `/queue/{namespace}/{topic}/backlog` endpoint. The
namespace and topic you want to monitor are `system` and `functions`, respectively. The response will look something
like this:

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
    {
      "partition": "persistent://tracardi/system/functions-partition-1",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-4",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-3",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-6",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-5",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-8",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-7",
      "subscription": "tracardi-function-subscription",
      "count": 0
    },
    {
      "partition": "persistent://tracardi/system/functions-partition-9",
      "subscription": "tracardi-function-subscription",
      "count": 0
    }
  ]
}
```

Ensure the `count` on each partition is low or equal to 0. This number tells how many messages are not consumer. Near
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

By default, Tracardi saves events in bulks to Elasticsearch with a bulk size of 500 events. Monitor if the background workers are filling
the predefined bulk size or if they trigger saving due to buffer timeout. Tracardi will save 500 events at once if they
arrive within a specific timeframe (e.g., 30 seconds). If not, the buffer will be emptied, and only the collected events
will be saved.

To ensure Elasticsearch can handle the data, define the number of nodes and the number of shards for the event index.
Changing the number of shards post-setup is not possible. When installing Tracardi use environment variables to configure at least
one data replica and set up shards for each index. Look for `ELASTIC_INDEX_REPLICAS` and `ELASTIC_INDEX_SHARDS`.

Proper scaling ensures that Tracardi can efficiently handle large volumes of data, providing a robust solution for
commercial needs.

# Wrap-up

Scaling may require several rounds of system adjustments. Please thoroughly test the configurations before going live. 