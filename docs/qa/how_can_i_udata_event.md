# How can I update event?

Events are typically considered immutable once they are created, as they represent a historical record of something that
occurred at a specific time. This immutability ensures data integrity and consistency. However, there are certain
scenarios where you might need to update event-related information, and the methods you mentioned are examples of how
this can be achieved:

1. **Elasticsearch Query:** While events themselves are immutable, you can use Elasticsearch queries to update event
   data.

2. **Change event during processing:** In Tracardi, there is a plugin that allow you to perform transformations or
   mappings on events in workflow. It is called `Copy data`. Confirm that you want to change event with `Update Event`
   action.

3. **Post Collection Event to Event Mapping:** Commercial Tracardi provides a feature called "post collection event to
   event mapping." This feature allows you copy values between event properties after its being collected.

## Update event by query

To update an event using an Elasticsearch query with the `update_by_query` API, follow these steps:

1. **Create the Query**: First, you need to construct the Elasticsearch query that specifies the documents (events) you
   want to update. This query should include the criteria to identify the events you want to modify and the changes you
   want to apply.

2. **Use the `update_by_query` API**: This API allows you to update documents in an index based on a query. It will find
   all documents matching the query and apply the specified changes to them.

Here's a general outline of the process:

1. **Construct the Query**: Your Elasticsearch query should be written in the JSON format and target the events you want
   to update. For example, if you want to update events with a certain attribute value, your query might look like this:

```json
{
  "query": {
    "term": {
      "attribute_name": "value_to_match"
    }
  }
}
```

2. **Define the Updates**: Within your query, you need to specify the changes you want to make to the selected events.
   This is done using the `script` parameter, which contains the code that will be executed for each matching event. For
   instance:

```json
{
  "query": {
    "term": {
      "attribute_name": "value_to_match"
    }
  },
  "script": {
    "source": "ctx._source.new_attribute = 'new_value'"
  }
}
```

3. **Execute the `update_by_query`**: Use the Elasticsearch API to execute the `update_by_query` operation. This can be
   done through various means, such as a command-line tool, a programming language's Elasticsearch library, or an HTTP
   client like cURL.

For example, using cURL:

```bash
curl -X POST "http://localhost:9200/your_event_index/_update_by_query" -H "Content-Type: application/json" -d '{
  "query": {
    "term": {
      "attribute_name": "value_to_match"
    }
  },
  "script": {
    "source": "ctx._source.new_attribute = 'new_value'"
  }
}'
```

Replace `your_event_index` with the name of your event index in Elasticsearch.

Keep in mind:

- Always be cautious when updating data. Test your queries on a small subset of data before applying them to a larger
  dataset.
- The Elasticsearch version you're using might have variations in the syntax or features of the `update_by_query` API.
  Check the Elasticsearch documentation for the version you're working with.

Lastly, ensure you have the necessary permissions and access to perform updates on your Elasticsearch index.