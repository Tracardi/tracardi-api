# Delete vector

Deletes a vector with a defined ID in the Weaviate schema.

## Description

The Delete vector plugin is used to delete a vector with a specified ID from the Weaviate schema. It connects to the
Weaviate instance and deletes the vector associated with the given ID. This plugin is useful for removing vectors that
are no longer needed or updating existing vectors in the Weaviate schema.

This documentation is for version 0.8.1 of the Delete vector plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the response from Weaviate if the vector deletion is successful. The response contains the data
  UUID of the deleted vector.
- **error**: Returns an error message if an error occurs during the execution of the plugin.

# Configuration

The Delete vector plugin has the following configuration parameters:

- **Weaviate Resource**: Select the Weaviate resource from the available options. This resource represents the Weaviate
  vector store.
- **Schema class**: Select the schema class from which the vector will be deleted. This class represents the type of
  data associated with the vector.
- **Object ID**: Type or reference the ID of the object for which the vector should be deleted. The object ID is
  required when deleting data from the schema.

# Required resources

This plugin requires the configuration of a Weaviate resource. The Weaviate resource represents the connection
information and credentials required to access the Weaviate instance.

# Errors

The Delete vector plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the execution of the plugin. The error message
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.