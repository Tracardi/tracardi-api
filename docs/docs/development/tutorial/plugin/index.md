# Code Workflow Plug-ins

Plug-ins are python classes which can be installed in Tracardi and become a part of Tracardi workflow.
Plug-ins are sometimes called actions or action plug-ins.

Below you will find information how to write plug-ins and how to install them in the system.

# Plug-in prerequisites

* Plug-in must return `Result` object. 
* Value inside `Result` object must be serializable to json.
* Value can not be bigger than x bytes.
* Value inside `Result` should be `dict` in order to be processed by other nodes.
* Plug-in must extend `ActionRunner` class.
* Resources that need closing should be closed in `close()` method.
* Async Method `set_up` should be used to initiate async objects.

# Plugin tutorials

* [Coding a plugin](part/part1.md)
* [Configuring the plugin](part/part2.md)
* [Referencing data in the plugin](part/part3.md)