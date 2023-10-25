# Query Local Database

This plugin provides the capability to execute queries on databases that reside within the local Elasticsearch instance.
It fetches data from specified indexes and can return queried data in the form of a result object.

# Version

This documentation was created for the plugin version 0.8.0.

## Description

The Query Local Database Plugin accepts an Elasticsearch data storage language (DSL) query and executes it on the local
Elasticsearch database. The plugin preprocesses the query to ensure there is a size specification and limits the
returned results to a maximum of 50 records per query. If there is no size specification, it defaults to 20 records per
query.

In addition to executing the query, this plugin can also log the query and its results. However, fetching more than 50
records might impact GUI performance and it is recommended to disable logging once tests are finished.

# Inputs and Outputs

The plugin takes one input:

- The **payload** object, which contains data that is sent to the plugin.

The plugin generates two types of outputs:

- **result**: This port returns the result from querying the ElasticSearch instance.
- **error**: This port returns an error message if one occurs during query execution, or if the returned result contains
  more than 20 records.

This plugin cannot act as a start point in the workflow.

# Configuration

The configuration parameters of this plugin are:

- **index**: This specifies the Elasticsearch index to be searched. This can be one of three types of indexes: Profile,
  Event, or Session.
- **query**: It takes in an Elasticsearch DSL query that needs to be executed on the database.
- **log**: This boolean variable determines whether or not the query execution is logged.

# JSON Configuration

Example of a JSON configuration object:

```python
{
    "index": "Profile",
    "query": "{\"query\":{\"match_all\":{}}}",
    "log": False
}
```

# Required resources

This plugin does not require any external resources to be configured.

# Errors

The errors that may be returned by this plugin and the conditions that might cause them are:

- Invalid Elasticsearch DSL queries: Syntax or structural errors in the DSL query may result in a JSONDecodeError. The
  JSONDecodeError message would provide further details about the error.
- Query execution issues: Errors that occur during the execution of a query would result in the __error__ output port
  being activated. The __value__ property of the Result object would contain an error message detailing the specific
  problem.