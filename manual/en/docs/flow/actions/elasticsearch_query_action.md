# Query Elasticsearch plugin

This plugin fetches data from given Elasticsearch resource.

## Requirements

Before using this plugin, you have to set Elasticsearch resource in Tracardi. You will have to provide the following
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

This plugin return search result on port **result** if search action was successful, or
empty payload on port **error** if error occurs. Error details are logged, please look for details on error in error log. 

## Configuration

#### Configuration in form

- *Elasticsearch resource* - here please provide your Elasticsearch resource.
- *Elasticsearch index* - here provide name of the index you wish to search.
- *Query* - here provide DSL query that you want to use to search provided index.

#### Configuration in JSON

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