# Part 1: Code simple plugin in Tracardi

Beginner Programmer's Guide

So, you would like to know how to add a new item to a workflow in the Tracardi system.
This article describes how a python programmer can extend Tracardi with new functions with so-called plugins.

## Introduction

Event handling in Tracardi is based on a __workflow__, which consists of individual __actions__ visualized as __nodes__
in the workflow. Workflow control when each action/node should be triggered. The action consists of an __input__, __a
program__ that computes the input data, and __an output__ (the result of the program computation). In tracardi, an action can have
one input and many outputs. In addition, the action has a configuration, it is a set of data that define how the program
should behave, Let's assume that we want to connect to external resources of some database, it is in the configuration
that we will have information about where this database is, and what username and password to use to connect to the
resource.

Due to the fact that Tracardi can have many outputs, we must somehow indicate on which output our data should appear.
That's why Tracardi introduces concepts such as a port. Thanks to them, we can indicate where the data will be returned.
The port that will not receive the data (returns the None value) causes that the workflow will not be performed in this
branch of the workflow.

## Development environment

!!! Info
    To start working with the system, we need to prepare a development environment. Refer to the
    [Python development environment](../../development/python_env.md) and read how
    to do this.

## Plugin life-cycle 

Plugins go through a life-cycle in which they are created, executed and recycled.

Workflow controls this process. When a workflow is created, the system recognizes which classes will be needed to start
the process defined in the data flow graph.

The process is as follows. The workflow checks what class is assigned to the node in the graph and checks if it exists.
It then creates its instances by running the parameterless `__init__` method of that class.

It then checks to see if there is an async set_up method. It passes the plug-in configuration to it. The configuration
is stored inside the node and is defined during plug-in registration (more on that in a moment). Then the workflow
executes nodes in the graph one by one and runs the `run(self, payload: dict, in_edge=None)` method, passing to it the
parameters that appeared at the input to the node and the additional information on the connection from the previous
node.

When the workflow exits, it executes the close method on each node.

In summary, we have the following methods in the plugin class.

```python
    __init__()  # (1)
    async set_up(config)  # (2)
    async run(input_payload)  # (3)
    async close()  # (4)
```

1. Initializes the plugin object
2. Set-ups the configuration and async resources
3. Gets the input payload as dictionary and runs the plugin, also returns results on ports
4. Closes async resources

!!! Info
    Please click (+) to see the comments for the code

## Our first plugin

We already have all the information so let's try to write the first plugin.

All plugins inherit from the ActionRunner class. This class stores the internal state of the workflow, i.e. elements
such as event data, profiles, etc. They can be useful for us while writing our plugin. Let's assume the simplest case,
we would like our workflow to react to the type of event that is sent to our system. It will check if the event is of
the type "my-event" and then it will return data from the input on the output named "MyEvent" otherwise it will return
empty data on the port "NotMyEvent".
Of-course we could use the built-in IF node, but we want to write our own.

## Let’s begin

Theoretically, we should complete all the methods described above, but in our case not all are needed. We don't have
configuration, so set_up method is not needed, we don't have connection to external systems, so close method is not
needed either, we don't have an internal state of class, so `__init__` will be empty.

Before we start, let's create a file in which we will write the code. The Tracardi plugins are in the directory:
`/tracardi/process_engine/action/v1`. You can create your own catalog there or use an existing one. I will create
my_plugin_folder directory and put my_plugin.py file in it.

### Now the code.

Our plugin could look like this:

=== "/tracardi/process_engine/action/v1/my_plugin_folder/my_plugin.py"

    ```python
    from tracardi.service.plugin.runner import ActionRunner
    from tracardi.service.plugin.domain.result import Result
    
    class MyPlugin(ActionRunner):  # (1)
        async def run(self, payload: dict, in_edge=None):  # (2)
            if self.event.type == "my-event":
                return Result(port="MyEvent", value=payload)  # (3)
            else:
                return Result(port="NotMyEvent", value={})  # (4)
    ```

    1. Extends ActionRunner class
    2. Runs the plugin
    3. Returns the input payload data on the "MyEvent" port 
    4. Returns the empty dictionary on the "NotMyEvent" port 

Note that we return the data using the `Result` class in which we provide the port name and value.

The only thing left for us to do is to describe the plugin in the system. This is done by defining a function called
`register`. It contains the specification of the plugin that we wrote (it returns the plugin class) and the type
metadata, with the input and output ports, the name of the plugin, etc.

The register function can be placed in the same file as the plugin or in any other file. I am placing it in the same
file.

#### Example:

=== "/tracardi/process_engine/action/v1/my_plugin_folder/my_plugin.py"

    ```python
    from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData

    def register() -> Plugin:
        return Plugin(   # (1)
            start=False,
            spec=Spec(  # (2)
                module=__name__,  # (4)
                className=MyPlugin.__name__,
                inputs=["payload"],
                outputs=["MyEvent", "NotMyEvent"],
                version='0.1',
                license="MIT",
                author="Your Name"
            ),
            metadata=MetaData(  # (3)
                name="My first plugin",
                desc='Checks if the event type is equal to my-event.',
                group=["Test plugin"]
            )
        )
    ```

    1. Returns Plugin class
    2. Sets spec property as Spec class
    3. Sets metadata property as Metadata class
    4. Sets `__name__` because refister is in the same file as plugin: e.i. `/tracardi/process_engine/action/v1/my_plugin_folder/my_plugin.py`

Let's analyze this code. It returns a plugin class that has the following properties.

* __start__ - sets whether the workflow can start from this node. In 99% of cases, we put `False` here. The startup
  nodes are already built into the system.
* __spec__ - describes the plugin specification, i.e. what class is to be run and what ports it contains on input and
  output. There can only be one port on input. In our case, we have the following data:
    * __module__ - where is the class package. `__name__` means that the class is in the same file as the register
      method.
      If we separate the plugin and register function, then you need to enter the package name of the plugin here, e.g.
      `tracardi.process_engine.action.v1.my_plugin_folder`
    * __className__ - the name of the class. We named it MyPlugin. See class `MyPlugin (ActionRunner)`
    * __inputs__ - list with the names of the input ports. There can only be one input port.
    * __outputs__ - list with names of output ports. Here we define what ports we have. Port names can have any name you
      like. Remember, however, that they must correspond to what the code returns and our code returns, one
      time: `Result (port="MyEvent", value=payload)` and another time `Result (port="NotMyEvent", value={})`, i.e. 
      possible output ports are `["MyEvent", "NotMyEvent"]`
    * __version__ - enter the plugin version here
    * __license__ - license type, Tracardi is able to attach the plug-in only under the `MIT` or `Apache 2.0` license
    * __author__ - author's first and last name
* __metadata__ - contains additional data about the plugin.
    * __name__ - the name of the plugin to be displayed on the workflow graph
    * __desc__ - a short description of what the plugin does
    * __group__ - plugins are displayed in groups. The name of the group in which the plug-in is to be displayed on the
      plug-in list. The name can be any or one of the existing names.

## Automatic plug-in loading.

The only thing left is to register the plug-in on the list of available plug-ins for installation. We do this by
pointing to the file with the register function.

To do that, go to the directory: `/tracardi/service/setup` and find the file `setup_plugins.py` This is the list of all
available plugins in the system.

At the top of this file you will find the variable `installed_plugins: Dict [str, PluginTestTemplate]` which is a
dictionary where the key is the location of the register function. The value is an object of the `PluginTestTemplate`
type, it is responsible for the test data for the plug-in. We will not write tests, so our block of code should look
like this:

=== "/tracardi/service/setup/setup_plugins.py"

    ```python
    "tracardi.process_engine.action.v1.my_plugin_folder.my_plugin": PluginMetadata(  # (1)
        test=PluginTest(init=None, resource=None)
    ),
    ```

    1. Key is the package of the register function

Type this into the `installed_plugins` dictionary, and we are ready to install the plugin.

Restart the Tracardi API so the changes are activated and go to `Processing/Workflows`, open any workflow and click the
`Reinstall Plugins` button. Alternatively you can go to `Maintenance/Plug-ins` and click the `Reinstall Plugins` button.

## Wrap-up

And this concludes the first part of the tutorial. We added the first plugin and installed it. In the second part we
will extend our plugin with the configuration form.
