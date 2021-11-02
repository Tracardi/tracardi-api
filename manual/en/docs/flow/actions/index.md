# Actions

Action is a single task in the workflow. Actions consist of input and output ports. Input ports are used to receive
data. On the other hand, output ports send data via connection to another action. Action is basically a code in the
system. Input ports are mapped to input parameters of a function in code when output ports are mapped to the return
values. Tracardi can be extended by programmers who write code and map it with action, which later on is visible in the
workflow editor as nodes.

## Action types

Actions can be divided into 2 distinctive types:

* *data processing action* - this type of action changes data and saves it in profile. Example of such action is action
  that copies data from event to profile.
* *connectors* - this type of actions connect to external databases and fetch or save data.

Although there are different types of actions the way they work is the same. they perform some task.

## Action Documentation

Below you wil find a list of action that are available in Tracardi. Documentaion shows how to configure those action using
JSON file. 