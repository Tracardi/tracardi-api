# Production installation scaling

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
environment variables to configure at least one data replica and set up shards for each index. Please look for `ELASTIC_INDEX_REPLICAS`, and `ELASTIC_INDEX_SHARDS`. 

### 4. Data Backup

For ElasticSearch data, using S3 storage for backups is recommended. This should be defined during the ElasticSearch
installation process to ensure data durability and availability. Please see Elasticsearch documentation for backup settings. 

### 5. Data Partitioning

Data partitioning is a critical strategy for managing large datasets. It involves dividing a database into distinct,
parts to improve manageability, performance, and availability. Please see this [documentation on data partitioning](data_partitioning.md).

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

Set the `AUTO_PROFILE_MERGING` and `INSTALLATION_TOKEN` to your custom values. See [guide on separating the APIs](guide.md).

### Conclusion

Deploying Tracardi in a production environment requires a detailed understanding of your performance needs and careful
configuration of various components. By following these recommendations, you can create a robust and scalable system
capable of handling your event processing and data management requirements efficiently. Continuously monitor and adjust
your setup to ensure optimal performance as your needs evolve.