# What could be the cause of the "Index index 'INDEX_NAME' was NOT CREATED" error during Tracardi update?

The "Index index 'INDEX_NAME' was NOT CREATED" error during Tracardi update occurs when the Elasticsearch server has
reached its maximum limit for open shards, preventing the creation of new indices. To resolve this error, it is
necessary to remove unused indices from Elasticsearch to free up resources for new indices.