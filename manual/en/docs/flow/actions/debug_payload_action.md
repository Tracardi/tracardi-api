# Debug payload

This node will read event by configured type and pass it to workflow.

# Configuration

Example configuration

```json
{
  "event": {
    "type": "page-view"
  }
}
```

It read first event that has type equal to "page-view". 
Then it assigns profile, session, and payload. If you connect it
to Start node it will pass this data to workflow and you can start debugging 
it with fetched data.

# Input

This node takes no input.

# Output

This node returns event on its output. Though the Start node will not read it.

# Side effects

This node runs only in debug mode. There is no need to remove it before 
deployment as it will be skipped in deployed workflow.  

