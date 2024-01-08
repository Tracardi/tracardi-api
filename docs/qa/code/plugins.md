# How to write some simple code of tracardi plugin

The purpose of writing code for a Tracardi plugin is to extend Tracardi's base functionalities by introducing new
actions or nodes to the existing workflow. By creating plugins, we can add features or functionality that control and
process the flow of data within Tracardi. These plugins can perform various tasks, such as data transformation, decision
making based on data properties, communication with external resources, or any custom functionality required by the
user.

Essentially, a plugin acts as an independent module within the Tracardi workflow system, representing a unit of work. A
plugin would have an input, a program that processes this input, and an output. In addition, plugins also have a
configuration that defines how they should behave, including information like how to connect to an external database.

Here's an example of a simple plugin:

This is a Python class representing a Tracardi plugin. The FlowWalker plugin scans the execution flow and processes each
node accordingly.

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result


class FlowWalker(ActionRunner):

    def __init__(self):
        pass

    async def set_up(self, config):
        pass

    async def run(self, payload: dict):
        input_data = payload.get('input', {})
        # process input_data here
        processed_data = {"output": "value"}
        return Result(port="payload", value=processed_data)

    async def close(self):
        pass


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=FlowWalker.__name__,
            inputs=["payload"],
            outputs=["payload"],
            version='0.7.1',
            license="MIT",
            author="Author"
        ),
        metadata=MetaData(
            name='FlowWalker',
            desc='Does nothing.',
            icon='error',
            group=["Events"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "payload": PortDoc(desc="This port returns given payload without any changes.")
                }
            )
        )
    )

```

Explanation of the code:

1. The `__init__` method initializes the plugin object. In this case, it does nothing.
2. The `set_up` method is used to set up and initialize resources. In this case, it's empty because no setup is
   required.
3. The `run` method is the main method of the plugin that is triggered in the workflow. It takes an input dictionary,
   processes it and returns the result. In this example, it simply reads the 'input' key from the dictionary, ignores
   it, and returns a new dictionary with an 'output' key and 'value' value.
4. The `close` method is used to close and clean up any resources. In this case it's empty because there are no
   resources to close.
5. `register` function registers delivers the information on how to register the plugin in the system.

Remember that as a developer, you can customize all of these methods to perform whatever actions you want, based on the
needs of your project or workflow.

# How to register a custom plugin in the system?

When you finished coding you custom plugin go to `tracardi/service/setup/setup_plugins.py` and add to

```python 
installed_plugins: Dict[str, PluginMetadata] 
```

the following line:

```python

"module-where-the-plugin-code-is-saved": PluginMetadata(
    test=PluginTest(
        init={},  # here your init data from spec
        resource={}  # here resource init data if exists
    ),
    plugin_registry="module-where-the-plugin-code-is-saved"
)

```

Replace the `module-where-the-plugin-code-is-saved` with the full path to module
like `tracardi.process_engine.action.v1.flow_walker` where the flow_walker is the python file.

Then click install plugin in the `Maintainace/Action Plugin-Ins` the button Plugins or Reinstall plugins.

# Write an example of plugin form

An exemplary plugin form in Tracardi could be the "Event type plugin configuration" that has been described in the
provided document. Here is its structure:

```python
Form(groups=[
    FormGroup(
        name="Event type plugin configuration",
        description="Define required event type",
        fields=[
            FormField(
                id="resource",
                name="Resource",
                description="Select your API resource.",
                component=FormComponent(type="resource", props={"label": "API Resource", "tag": "api"})
            ),
            FormField(
                id="event_type",
                name="Event type",
                description="Event type to check",
                component=FormComponent(type="text", props={"label": "Event type"})
            )
        ]
    )
])
```

The plugin form contains two main fields:

1. `Resource` - This allows users to select the API resource for their plugin. This field is created using a
   FormComponent with a type of "resource". The "label" and "tag" properties for this field indicate the way the field
   will be displayed in the GUI.

2. `Event type` - This field enables users to specify the event type their plugin should target. It is created using
   another FormComponent but with a type of "text". This component also has a "label" property which determines how the
   field will be presented in the GUI.

By extending the plugin form with these fields, users can specify a resource and event type for their plugin, tailoring
it to their specific use case.

The form array should be referenced in `register` function in Plugin object property `spec.form` like this:

```python

from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData
from tracardi.service.plugin.domain.register import Form, FormGroup, FormField, FormComponent  # 

# this is the function that will be called to get the data of plugin when it is registered.
def register() -> Plugin:
    return Plugin(

        start=False,
        spec=Spec(
            module=__name__,
            className='MyPlugin',
            init={
                "event_type": ""
            },
            form=Form(groups=[
                FormGroup(
                    name="Event type plugin configuration",
                    description="Define required event type",
                    fields=[
                        FormField(
                            id="resource",
                            name="Resource",
                            description="Select your API resource.",
                            component=FormComponent(type="resource", props={"label": "API Resource", "tag": "api"})
                        ),
                        FormField(
                            id="event_type",
                            name="Event type",
                            description="Event type to check",
                            component=FormComponent(type="text", props={"label": "Event type"})
                        )
                    ]
                )
            ]),
            inputs=["payload"],
            outputs=["MyEvent", "NotMyEvent"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        metadata=MetaData(
            name="My first plugin",
            desc='Checks if the event type is equal to my-event.',
            group=["Test plugin"]
        )
    )

```

# What is plugin form?

The plugin form is part of plugin code where you define the configuration of the plugin. Basically plugins can be
configured with JSON objects. Forms map the form fields with the JSON. When changes are made within the form, it is
reflected in the JSON configuration and vice-versa.

For instance, when we have a form like this

```python
form = Form(groups=[
   FormGroup(
      name="Event type plugin configuration",
      description="Define required event type",
      fields=[
         FormField(
            id="resource",
            name="Resource",
            description="Select your API resource.",
            component=FormComponent(type="resource", props={"label": "API Resource", "tag": "api"})
         ),
         FormField(
            id="event_type",
            name="Event type",
            description="Event type to check",
            component=FormComponent(type="text", props={"label": "Event type"})
         )
      ]
   )
]),
```

and JSON configuration like this:

```json
init={
   "resource": {
      "id": "",
      "name": ""
   },
   "event_type": {
      "id": "",
      "name": ""
   }
}
```

That means the `FormGroup` "Event type plugin configuration" is created with two `FormField`s: "Resource" and "Event
type". The `id` of a `FormField` must match with a configuration property in `init`, allowing for a connection between the form
value and the configuration value. This is explained as "This is how you bind configuration with the form field." in the
documentation.

# What is a simple code template for custom plugin?

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result


class FlowWalker(ActionRunner):

   def __init__(self):
      # Init data here 
      pass

   async def set_up(self, config):
      # setup resource if needed
      pass

   async def run(self, payload: dict):
      # process and return data
      return Result(port="payload", value=payload)

   async def close(self):
      # close all open connections
      pass

# Register plugin
def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,  # Module name
            className=FlowWalker.__name__,  # Class Name
            inputs=["payload"],  # input ports, must be one
            outputs=["payload"],  # output ports, may be many
            version='0.7.1',
            license="MIT",
            author="Author"
        ),
        metadata=MetaData(
            name='FlowWalker',  # Plugin name
            desc='Does nothing.',  # Plugin description
            icon='error',  # Icon
            group=["Events"],  # Group in the menu
            documentation=Documentation(  # Port documentation
                inputs={  # Documentation for input port. We defined that input port is named 'payload`
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={ # Documentation for output port. We defined that output port is also named 'payload`
                    "payload": PortDoc(desc="This port returns given payload without any changes.")
                }
            )
        )
    )

```

Notice that `outputs=["payload"]` matches the `return Result(port="payload", value=payload)` and 

```python
outputs={ "payload": PortDoc(desc="This port returns given payload without any changes.") }
```

The same with `inputs=["payload"]` that matches: 

```python
inputs={  "payload": PortDoc(desc="This port takes payload object.") }
```

in the documentation propery of object metadata.