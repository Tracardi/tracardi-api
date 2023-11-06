# Your task

Your task is to develop a Tracardi plugin. Your objective is to construct a functional Tracardi plugin using
the guidelines presented `General context`, and in a 3-part series of `Plugin tutorials`. Each part of these tutorials
elucidates various aspects of Tracardi plugins.

To accomplish this task, you are expected to assimilate knowledge from `General context` and the tutorials and utilize
the
information specified in the "Your goal" section. Your primary aim is to write a single file code plugin that achieves
the functionality
described in the "Your goal" section. Include all necessary classes and functions like Configuration, registration,
validation, etc.
Plugin must return data only on ports. Do not write any explanation just code.

# General context

Tracardi plugins are used in workflows. They are sometimes called actions or action plugins. Workflow passes data form
plugin to plugin via its input and output ports. Plugin may have one input port and many output ports.

Workflow has internal state. It can be referenced byt the dot notation. In
short, dot notation is a way of referencing data in Tracardi. It is used to access data from the internal state of the
workflow, such as the event, profile, payload, flow, session, and memory. It is written in the form of <source>@<
path.to.data>, where the source is the type of data you are referencing and the path is a string of keys that indicate
where the data is located. Class DotAccessor is used to access dot notated data. Usually the DotAccessor dict is
returned by `self._get_dot_accessor(payload)`. DotAccessor extends dict and acts as dict.

Plugin is documented so it has MetaData class with properties like `name`, `desc`, `documentation`. PortDoc class
describes
in desc property the value returned on the port.

## How the code is organized:

The main logic of the plugin is located in the "run" method, which accepts a dictionary called "payload" as input. The
plugin's configuration is defined in the "register" method within the "Plugin" object, specifically in the "spec.init"
property. To understand the purpose of each configuration key, refer to the "FormField" description property found
within the "Plugin" property under "form.group.field.id". Use the corresponding ID in the FormField description to
enhance the documentation for the payload. The configuration is used to set up the plugin's functionality.

The "run" method returns a Result object with two properties port and value.
The value of the port is the result of executing the plugin. The port describes the output port of the plugin in the
workflow.
The description of the port and its value can be found in the metadata.documentation.outputs section.

# Plugin tutorials

## Introduction

In this tutorial, we will learn how to create a plugin for Tracardi, an open-source automation tool designed for
processing and analyzing data. Plugins in Tracardi extend its functionality by allowing users to define custom actions
and transformations. This guide will take you through the process of creating a basic Tracardi plugin using Python.

## Creating a Simple Tracardi Plugin

In this part, we'll create a simple Tracardi plugin that checks if an event type matches a predefined value.

### Writing the Plugin Code

Now, let's write the code for your Tracardi plugin.

plugin inherits from: 

```python
class ActionRunner:

    @final
    def __init__(self):
        pass

    async def set_up(self, init):
        pass

    async def run(self, payload: dict, in_edge=None):
        pass

    async def close(self):
        pass
```

And can look like this.


```python
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result


class MyPlugin(ActionRunner):

    async def run(self, payload, in_edge=None):
        if self.event.type == "my-event":
            return Result(port="MyEvent", value=payload)
        else:
            return Result(port="NotMyEvent", value={})
```

This code defines a simple plugin that checks if the event type is "my-event." If it is, the plugin returns a Result
with the port "MyEvent," and if not, it returns a Result with the port "NotMyEvent."

This is the definition of a Result class:

```python
from typing import Optional
from pydantic import BaseModel

class Result(BaseModel):
    port: str
    # Notice that value be either None or dict.
    value: Optional[dict] = None
```

So when you return an error message always return it like this: 

```python
from tracardi.service.plugin.domain.result import Result
try:
    pass
    # Some code
except Exception as e:
    return Result(port="error", value={"message": str(e)})
```

### Registering the Plugin

To register your plugin with Tracardi, you need to define the plugin's metadata add the following code at the bottom:

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc


def register() -> Plugin:
    return Plugin(
        spec=Spec(
            module=__name__,
            className='MyPlugin',
            inputs=["payload"],
            outputs=["MyEvent", "NotMyEvent"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        # This is plugin documentation. 
        metadata=MetaData(
            name="My First Plugin",
            desc='Checks if the event type is equal to my-event.',
            group=["Test Plugin"],
            # Notice that outputs key are the same as spec.outputs and are the same as Result.port.
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "MyEvent": PortDoc(desc="Description of what is returned on the output port MyEvent"),
                    "NotMyEvent": PortDoc(desc="Description of what is returned on the output port NotMyEvent")
                }
            ),
        )
    )
```

This code registers the plugin with Tracardi and provides essential information such as the plugin's name, description,
inputs, and outputs.

## Configuring the Plugin in Tracardi

In this part, we'll learn how to configure and validate the plugin data and add a configuration form to it.
We'll also make the plugin more flexible by allowing users to specify the event type to check.

### Extending the Plugin Code

Let's update the plugin code to make it configurable.

```python
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    event_type: str


def validate(config: dict):
    return Configuration(**config)


class MyPlugin(ActionRunner):
    # Set the configuration property
    config: Configuration

    async def set_up(self, config):
        # Validate with pydantic Configuration class
        self.config = validate(config)

    async def run(self, payload, in_edge=None):
        if self.event.type == self.config.event_type:
            return Result(port="MyEvent", value=payload)
        else:
            return Result(port="NotMyEvent", value={})
```

In this code, we added a `set_up` method that initializes the `event_type` variable from the plugin's configuration.

### JSON Configuration

To make the plugin configurable, we need to define the configuration options. Open the `setup.py` file and modify
the `register` function like this:

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc


def register() -> Plugin:
    return Plugin(
        spec=Spec(
            module=__name__,
            className='MyPlugin',
            init={
                "event_type": "my-event"
            },
            # Plugins must always take only one input, that is payload and is the output from the previous node in workflow.
            inputs=["payload"],
            outputs=["MyEvent", "NotMyEvent"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        metadata=MetaData(
            name="My First Plugin",
            desc='Checks if the event type is equal to my-event.',
            group=["Test Plugin"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "MyEvent": PortDoc(desc="Description of what is returned on the output port MyEvent"),
                    "NotMyEvent": PortDoc(desc="Description of what is returned on the output port NotMyEvent")
                }
            ),
        )
    )
```

We added the `init` parameter, which defines the default configuration for the plugin. Here, we set the
default `event_type` to "my-event."

### Plugin Form

Let's add a configuration form to the plugin to make it easier for users to configure it. Update the `setup.py` file as
follows:

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.domain.config import PluginConfig


class Configuration(PluginConfig):
    event_type: str


def validate(config: dict):
    return Configuration(**config)


class MyPlugin(ActionRunner):
    config: Configuration

    async def set_up(self, config):
        # Validate with pydantic Configuration class
        self.config = validate(config)

    async def run(self, payload, in_edge=None):
        if self.event.type == self.config.event_type:
            return Result(port="MyEvent", value=payload)
        else:
            return Result(port="NotMyEvent", value={})


def register() -> Plugin:
    return Plugin(
        spec=Spec(
            module=__name__,
            className=MyPlugin.__name__,
            init={
                "event_type": "my-event"
            },
            form=Form(groups=[
                FormGroup(
                    name="Plugin Configuration",
                    fields=[
                        FormField(
                            id="event_type",
                            name="Event Type",
                            description="Event type to check",
                            component=FormComponent(type="text", props={"label": "Event Type"})
                        )
                    ]
                ),
            ]),
            inputs=["payload"],
            outputs=["MyEvent", "NotMyEvent"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        metadata=MetaData(
            name="My First Plugin",
            desc='Checks if the event type is equal to my-event.',
            group=["Test Plugin"]
        )
    )
```

In this code, we've added a configuration form with a single text field for specifying the event type. The `id`
and `name` attributes should match the configuration key we defined earlier in the `init` section.

Notice that we used:

```python

```

But thee are also other types of form field. For example select when you have a defined set of data and user should not
select any other value then defined in select.

Example usage of select form field, Where key is a `operation` available value and dict value is a Label in select.

```python
FormField(
    id="operation",
    name="Min/Max",
    description="Select what value you would like to find.",
    component=FormComponent(type="select", props={
        "label": "Min/Max",
        "items": {
            "min": "Min Value",  # Key is `operation` value and Value is a Select Label
            "max": "Max Value" # Key is `operation` value and Value is a Select Label
        }
    })
)
```

If the variable seems to get any data use text form field.

Example:

```python
FormField(
    id="event_type",
    name="Event Type",
    description="Event type to check",
    component=FormComponent(type="text", props={"label": "Event Type"})
)
```

If the data is used with DotAccessor use dotPath.

Example:

```python
FormField(
    id="set2",
    name="Set 2",
    description="Reference to the second set data.",
    component=FormComponent(type="dotPath", props={"label": "Set 2"})
)
```


## Data Reference

In order to reference the data from internal state of the workflow you need to use DotAccessor.
Lets assume that our event type is not a string but a dot notated path to data. To get the value itself you need to use
DotAcessor.

```python
from tracardi.service.plugin.domain.result import Result


async def run(self, payload: dict, in_edge=None):
    # Get the DotAccessor object that will convert the dot notation to the data. 
    dot = self._get_dot_accessor(payload)
    # Convert anything that is defined in `self.config.event_type` to the real data from the workflow internal state and assign it to value
    value = dot[self.config.event_type]

    if self.event.type == value:
        return Result(port="MyEvent", value={"result": True})
    else:
        return Result(port="NotMyEvent", value={"result": False})
```

### Creating a Resource

In some cases, you may need to connect your plugin to external resources. Let's create a resource that will allow the
plugin to send data to a user-defined API.

#### Define the Resource

Here's an example of a resource configuration:

```python
from pydantic import BaseModel, AnyHttpUrl, Optional


class MyApiResourceConfig(BaseModel):
    url: AnyHttpUrl
    method: str
    api_key: Optional[str] = None
```

This configuration defines the API URL, HTTP method, and an optional API key.

#### Load the Resource in the Plugin

To use the resource in your plugin, you can load it in the `set_up` method. Add the following code to
your `my_plugin.py` file:

```python
from tracardi.service.storage.driver.elastic import resource as resource_db


class MyPlugin(ActionRunner):

    async def set_up(self, config):
        # The same as before
        self.config = validate(config)

        # Now add resource
        resource = await resource_db.load(self.config.resource.id)
        self.api_credentials = resource.credentials.get_credentials(self, output=MyApiResourceConfig)
```

This code loads the resource based on the `self.config.resource.id` and extracts the API credentials as
a `MyApiResourceConfig` object.

### Step 4: Configuring the Resource Select Field

The last step is to add a field to your plugin's form that allows users to select a resource from the list of defined
resources. You can use the `resource` component in the form. Update the `setup.py` file like this:

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent


def register() -> Plugin:
    return Plugin(
        spec=Spec(
            module=__name__,
            className='MyPlugin',
            init={
                "event_type": "event@path.to.my-event",
                "resource": {
                    "id": "",
                    "name": ""
                }
            },
            form=Form(groups=[
                FormGroup(
                    name="Plugin Configuration",
                    fields=[
                        FormField(
                            id="event_type",
                            name="Event Type",
                            description="Event type to check",
                            # Component of dotPath use a dotted notation typed by user so always use dotPath if it will go 
                            # through dotAccessor class. Otherwise use text.
                            component=FormComponent(type="dotPath", props={"label": "Event Type"})
                        ),
                        FormField(
                            id="resource",
                            name="Resource",
                            description="Select your API resource.",
                            component=FormComponent(type="resource", props={"label": "API Resource", "tag": "api"})
                        )
                    ]
                ),
            ]),
            inputs=["payload"],
            outputs=["MyEvent", "NotMyEvent"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        metadata=MetaData(
            name="My First Plugin",
            desc='Checks if the event type is equal to my-event.',
            group=["Test Plugin"]
        )
    )
```

In the form definition, we added a field named "resource" that uses the `resource` component type and has the tag "api"
to filter resources related to your plugin.

# Your goal

Write a Tracardi plugin to address the need for a plugin that returns the date bases on time delta. 
Date must be computed using the time delta that is delivered by the user in the plugin form And this is the only configuration that the user must deliver. 
Current time is added to a defined delta and the date is returned on the result port. If there is an error it is returned on error port.