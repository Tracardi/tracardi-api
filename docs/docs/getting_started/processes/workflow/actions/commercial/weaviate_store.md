# Store vector

Stores a vector in Weaviate. This plugin can create or update a vector in the Weaviate Vector Store.

## Description

The Store vector plugin is used to store a vector in the Weaviate schema. It connects to the Weaviate instance and
performs the specified operation (insert or update) on the vector based on the provided configuration. The plugin
accepts a payload object as input and stores the vector in the specified schema class.

This documentation is for version 0.8.1 of the Store vector plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the response from Weaviate after storing the vector.
- **error**: Returns an error message if an error occurs during the execution of the plugin.

# Configuration

The Store vector plugin has the following configuration parameters:

- **Weaviate Resource**: Select the Weaviate resource from the available options. This resource represents the Weaviate
  vector store.
- **Schema class**: Select the schema class in which to store the vector. This class represents the type of data
  associated with the vector.
- **Operation**: Select the type of operation to perform on the vector. The available options are "Insert" and "Update".
- **Object ID**: Type or reference the ID of the object for which the vector should be stored. The object ID is required
  for update operations.
- **Data object**: Provide the vector data as a JSON object. This object represents the vector to be stored in Weaviate.

# Required resources

This plugin requires the configuration of a Weaviate resource. The Weaviate resource represents the connection
information and credentials required to access the Weaviate instance.

# Errors

The Store vector plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the execution of the plugin. The error message
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.