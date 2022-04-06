# Elasticsearch query plugin

This plugin fetches data from Elasticsearch.

## Requirements

It requires a configured Elasticsearch resource in Tracardi. You will have to provide the following
information to connect to elastic:

```json
{
  "url": "<url>",
  "port": 9200,
  "scheme": "http",
  "username": "<username>",
  "password": "<password>",
  "verify_certs": true
}
```

## Input

This plugin takes any payload as input.

## Output

This plugin returns search result on port **result** if search was successful, or
empty payload on port **error** if error occurs.  

## Configuration

#### Form fields

- *Elasticsearch resource* - your Elasticsearch resource.
- *Elasticsearch index* - name of the index you wish to search.
- *Query* - DSL query to search with configured index.

#### JSON Configuration

```
{
  "source": {
    "name": "<name-of-your-elasticsearch-resource>",
    "id": "<your-elasticsearch-resource-id>"
  },
  "index": "<name-of-your-index>",
  "query": <your-dsl-query>
}
```