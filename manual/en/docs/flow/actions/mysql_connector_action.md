# Mysql Connector

This plugin connects to Mysql and executes a SQL query.

# Configuration

*Example*

```json
{
  "source": {
    "name": "mysql",
    "id": "a8430a5c-43de-44eb-9c25-2b1426aed3a0"
  },
  "type": "select",
  "query": "SELECT * FROM user WHERE User=%s;",
  "data": [
    "root"
  ],
  "timeout": 10
}
```

* *source* this a resource with MySQL credentials. See below for credentials schema.
* *type* - type of query, possible values are ['select', 'insert', 'delete', 'update']
* *query* - this is the SQL prepared statement. It will replace %s with data provided in *data* key. This is a
  sequential order so order of %s and data matters.
* *data* - data to replace in SQL prepared statement template.
* *timeout* - query timeout.

# Output

It returns the data in JSON.

*Example*

```json
{
  "result": [
    {
      "Host": "%",
      "User": "root",
      "Select_priv": "Y",
      "Insert_priv": "Y",
      "Update_priv": "Y",
      "Delete_priv": "Y",
      "Create_priv": "Y",
      "Drop_priv": "Y"
    },
    {
      "Host": "localhost",
      "User": "root",
      "Select_priv": "Y",
      "Insert_priv": "Y",
      "Update_priv": "Y",
      "Delete_priv": "Y",
      "Create_priv": "Y",
      "Drop_priv": "Y"
    }
  ]
}
```

If the query is of insert type then the output result will have last inserted record id.

If the query is of type "delete","update", or "create" then the output result will have input payload.

# Errors

```
Not all arguments converted during string formatting
```

This error is raised when the number of %s placeholders and data do not match. That means the number of placeholders is
not equal to the number of data.
