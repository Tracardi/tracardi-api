# Mongo connector

This plugin connects to mongo and queries this database.

# Configuration

```json
{
  "source": {
    "name": "MongoDB",
    "id": "fbabb00e-a724-40bf-b889-bd8d6a7f25e2"
  },
  "database": "my_database",
  "collection": "my_collection",
  "query": "{}"
}
```

* *database* - database name.
* *collection* - mongodb collection.
* *query* - mongodb query.

# Input

This node does not process input payload.

# Output

Query result.
