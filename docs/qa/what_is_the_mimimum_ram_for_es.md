# What is the minimum RAM for Elasticsearch to run Tracardi?

The absolute minimum RAM for Elasticsearch to run Tracardi is 2GB per node. However, it's crucial to understand that
this is far from optimal for production use.

Tracardi leverages Elasticsearch for handling big data operations, which demands significant resources for efficient
performance. In a production environment, it's highly recommended to deploy at least 3 Elasticsearch nodes for
redundancy and data distribution.

For optimal performance, each node should have as much memory as you can allocate. A more realistic minimum for a
production setup would be:

- 3 nodes
- 8GB RAM per node (24GB total)

Remember, this is still a conservative estimate. In scenarios dealing with large datasets or high query volumes, you
might need 16GB, 32GB, or even more RAM per node. The more memory you can provide, the better Elasticsearch will
perform, especially when handling the big data operations that Tracardi requires.

Always monitor your Elasticsearch cluster's performance and be prepared to scale up resources as your data volume and
processing needs grow.