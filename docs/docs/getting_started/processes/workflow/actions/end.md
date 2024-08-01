# End

The End plugin can be used to terminate the workflow. It is designed to wrap the entire process of a workflow and
provide the last action.

# Version

The current plugin version is 0.1.

## Description

End plugin functions as a termination point for the workflow, halting the flow of data. The operation inside the 'run'
method of this plugin is simple: it accepts a payload as an input and does not return anything, signifying the end of
the workflow. The plugin does not modify the execution graph which means there's no update to the internal state of the
workflow (event, profile, session).

# Inputs and Outputs

The End plugin has one input port:

- __payload__: This port accepts a payload object. An example of a payload object can be a dictionary that holds data
  passed in the workflow.

This plugin does not generate any output, hence no output ports.

# Configuration

The End plugin does not require any configuration. Its functionality is predefined.

# JSON Configuration

No configuration is required for this plugin, thus no JSON example is provided.

# Required resources

The End plugin does not require any external resources to be configured.

# Errors

The End plugin does not throw any specific exceptions.
