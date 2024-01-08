# Get Event Source Plugin

The Get Event Source Plugin is part of the Input/Output group and is primarily used for tasks related to data collection
or segmentation. Its function is to read the source that the event came from.

# Version

The current version of this plugin is 0.6.0.1.

## Description

The Get Event Source Plugin is designed to read and return the source from which the event originated. It does this by
loading the id of the source associated with the event.

In the event where the source does not exist, the plugin returns an error message indicating that the source does not
exist. If the source is found, the plugin proceeds to return a dump of the loaded source model.

# Inputs and Outputs

This plugin only accepts one input port, named "payload". As for the output ports, the plugin offers two; 'source' and '
error'.

- The **Input**, "payload", reads a payload object.
- The **Output**, "source", gives back the data of the source in case it is found and loaded successfully.
- The **Output**, "error", returns an error message in case the source is not found or another error occurs during the
  process of loading the source.

This plugin does not initiate the workflow.

# Configuration

This plugin does not require any configuration.

# JSON Configuration

Since this plugin does not require any configuration, no configuration example is provided.

# Required resources

This plugin does not require any external resources to be configured.

# Errors

Error that might be encountered during the operation of this Plugin is:

- "Source __{}__ does not exist.": This indicates that the source associated with the event's id does not exist in the
  system. This error occurs when one tries to load a non-existing source.