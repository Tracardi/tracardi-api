# Vector exists

Checks if a vector with a defined ID exists in the Weaviate schema.

## Description

The Vector exists plugin is used to check if a vector with a specified ID exists in the Weaviate schema. It connects to
the Weaviate instance and verifies the presence of the vector associated with the given ID. This plugin is useful for
conditional branching in workflows based on the existence of vectors in the Weaviate schema.

This documentation is for version 0.8.1 of the Vector exists plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has three outputs:

- **true**: Returns the payload if the vector with the defined ID exists in the Weaviate schema.
- **false**: Returns the payload if the vector with the defined ID does not exist in the Weaviate schema.
- **error**: Returns an error message if an error occurs during the execution of the plugin.

# Configuration

The Vector exists plugin has the following configuration parameters:

- **Weaviate Resource**: Select the Weaviate resource from the available options. This resource represents the Weaviate
  vector store.
- **Schema class**: Select the schema class to check for the existence of the vector. This class represents the type of
  data associated with the vector.
- **Object ID**: Type or reference the ID of the object for which the vector existence should be checked. The object ID
  is required when checking the existence of data in the schema.

# Required resources

This plugin requires the configuration of a Weaviate resource. The Weaviate resource represents the connection
information and credentials required to access the Weaviate instance.

# Errors

The Vector exists plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the execution of the plugin. The error message
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.