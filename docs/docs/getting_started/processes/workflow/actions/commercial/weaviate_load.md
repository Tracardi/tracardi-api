# Load vector

Loads a vector by ID from Weaviate.

## Description

The Load vector plugin is used to retrieve a vector from the Weaviate schema based on the specified ID. It connects to
the Weaviate instance and fetches the vector associated with the given ID. This plugin is useful for retrieving vectors
from the Weaviate schema for further processing in Tracardi workflows.

This documentation is for version 0.8.1 of the Load vector plugin.

# Inputs and Outputs

This plugin has one input:

- **payload**: This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the loaded vector from Weaviate as a response object.
- **error**: Returns an error message if an error occurs during the execution of the plugin.

# Configuration

The Load vector plugin has the following configuration parameters:

- **Weaviate Resource**: Select the Weaviate resource from the available options. This resource represents the Weaviate
  vector store.
- **Schema class**: Select the schema class from which to load the vector. This class represents the type of data
  associated with the vector.
- **Object ID**: Type or reference the ID of the object for which the vector should be loaded. The object ID is required
  to fetch the associated vector from Weaviate.

# Required resources

This plugin requires the configuration of a Weaviate resource. The Weaviate resource represents the connection
information and credentials required to access the Weaviate instance.

# Errors

The Load vector plugin may encounter the following error:

- **Error**: This error occurs when an exception is raised during the execution of the plugin. The error message
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.