# Microservice

This plugin allows you to execute a plugin that resides on a remote microservice. The Microservice plugin sends a
payload to a remote server where the actual plugin code is run, and then captures the results of the execution.

# Version

0.7.2

## Description

The Microservice plugin forwards the payload and some other information (called "context") about the environment in
which the plugin is running to a remote server. The specific plugin that will process the payload is identified by
the **service_id** and **action_id**. All the information sent to the remote server is packed into a dictionary and encoded
as a JSON string.

This JSON string is then sent to the specified URL using a **POST** HTTP request. When the response arrives from the
remote server, it is returned as the plugin's result.

The plugin returns two types of ports, either "response" or "error". The value of the port is determined at runtime
depending on the outcome of the remote server's execution. The "response" port is returned if the remote server
successfully processed the payload, and "error" is returned if it failed to process the payload.

The remote server is responsible for updating the workflow's internal state with new information from the request's
context.

# Inputs and Outputs

The Microservice plugin only manages one input port named "payload". This is the input data that the plugin will forward
to the remote server for processing.

Here is an example of an input JSON:

```json
{
  "payload": {
    "data-key": "data-value"
  }
}
```

This plugin has two output ports: "response" and "error". The response port is triggered when the communication with the
remote server is successful, and returns the data returned by the remote server, and the error port is triggered when
the communication failed, it returns the error information.

The returned values can be like this (example in JSON format):

```json
{
  "response": {
    "result": {
      "key1": "value1",
      "key2": "value2"
    },
    "context": {
      "session": {
        "id": "abc123",
        "startTime": "1641326491"
      },
      "profile": {
        "id": "def456",
        "timestamp": "1641326491"
      }
    },
    "console": {
      "logs": [
        "log1",
        "log2",
        "log3"
      ]
    }
  },
  "error": {
    "message": "An error occurred while processing the request."
  }
}
```

# Configuration

This plugin does not require any special configuration.

# JSON Configuration

This plugin does not have any configuration inputs, thus there is no JSON Configuration required.

# Required resources

The Microservice plugin requires an external resource, a remote server with the specified **url** and **token**.

# Errors

- "Plugin {node.microservice.plugin.name} not implemented correctly. It must return result either on port response or
  error, returned data on port {result.port}. This error occurs when the remote server returns result on a port other
  than "response" or "error".

- If the remote server returns a HTTP Status different from 200, the error port is triggered and the response from the
  server is returned as the error. For example, when a 404 status is returned, it means that the requested resource
  could not be found on the remote server. Other status codes represent other types of HTTP errors.