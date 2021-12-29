# Action's Core Definitions

Action is a single task in the workflow. Actions consist of input and output ports. Input ports are used to receive
data. On the other hand, output ports send data via connection to another action. Action is basically a code in the
system. Input ports are mapped to input parameters of a function in code when output ports are mapped to the return
values. Tracardi can be extended by programmers who write code and map it with action, which later on is visible in the
workflow editor as nodes.

## Action ports

Action node can have only one input port and many output ports. Port that return no data (Python: None) will not 
trigger the next node execution.

## Action internal state

Each action node has a reference to the following data:

* *id* - node id
* *debug* - flag that tells if the node is in the debug mode
* *event* - currently processed event
* *profile* - currently processed profile. Profile may be empty if the event that is being processed is a profile less 
* event. Search for profileless events in the documentation.
* *session* - current user session
* *flow*  - flow diagram
* *execution_graph* - information on graph execution, with nodes that have referenced action class instances. 
* *node* - information on current executing node. With information on the inbound and outbound edges.
* *console* - the object where you can log error and warnings.
* *metrics* - metrics object

## Accessing internal state

Actions use dot notation to access the internal state of the node. Some date is not available via dot notations. See
[dot notation](../../notations/dot_notation.md) for details.


## Action core methods

Action node has 3 core methods:

* *build* - asynchronous method for action building
* *__init__* -  synchronous action constructor
* *run* - methods that runs the action 

## Auxiliary functions

Action should also have a set of auxiliary functions that help Tracardi with acton registration and data validation. 
Those functions are:

* *register* - it should return a Plugin object with information on action specification (where is it located in code, 
  what class should Tracardi run, where is the documentation etc.), metadata (how to present the action in the workflow, 
  its icon, configuration form , etc.)
* validate -  how to validate the configuration data

## Action Documentation

Below you will find a list of action that are available in Tracardi. Documentation shows how to configure those action using
JSON file. GUI user can configure actions by filling the form. 