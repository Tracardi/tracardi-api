# Plugins

Plugins are python classes which can be installed in Tracardi and they become parts of Tracardi workflow.

Below you will find information how to write plugins and how to install them in the system.

# Plugin prerequisites

* Plugin must return Result object. 
* Value inside Result object myst be serializable to json.
* Value can no tbe bigger then x bytes.
* Value inside Result should be dict in order to be processed by other nodes.
* Plugin must extend ActionRunner class.
* Resources that need closing should be closed in close methos.
* Static method build should be used to initiate async objects.