# Your task

You have been assigned the task of documenting the Tracardi plugin.

Your goal is to create clear and understandable documentation for non-technical individuals who may not be familiar with
terms like variable or class. You will be provided with the plugin's code and an available manual (if available), which
you should incorporate into a single, consistent documentation in Markdown format.

The documentation should begin with the plain plugin name not `Tracardi Plugin Documentation:`. Do not mention that user
has to refer to the Tracardi documentation for more information (the generated text is the documentation).

Use only plain English to describe the code and its components. Avoid including any code or plugin metadata in the
documentation, except where necessary for clarity. Use the logic from the code to describe its purpose and how it works. 

Include information about returned exceptions and errors and the condition when they may occur. Document it in `Errors`
section with all the exceptions (meaning exception message) and the condition when they may occur. 

Include the return data schema if possible.

# General context

Tracardi plugins are used in workflows. They are sometimes called actions or action plugins. Workflow passes data form 
plugin to plugin via its input and output ports. Plugin may have one input port and many output ports. 

Workflow has internal state. It can be referenced byt the dot notation. In
short, dot notation is a way of referencing data in Tracardi. It is used to access data from the internal state of the
workflow, such as the event, profile, payload, flow, session, and memory. It is written in the form of <source>@<
path.to.data>, where the source is the type of data you are referencing and the path is a string of keys that indicate
where the data is located. Class DotAccessor is used to access dot notated data. Usually the DotAccessor dict is
returned by `self._get_dot_accessor(payload)`. DotAccessor extends dict and acts as dict.

Workflow can also execute UX plugins that in return will inject some javascript to the page where the Tracardi 
integration script is placed.

# How the code is organized:

The main logic of the plugin is located in the "run" method, which accepts a dictionary called "payload" as input. The
plugin's configuration is defined in the "register" method within the "Plugin" object, specifically in the "spec.init"
property. To understand the purpose of each configuration key, refer to the "FormField" description property found
within the "Plugin" property under "form.group.field.id". Use the corresponding ID in the FormField description to
enhance the documentation for the payload. The configuration is used to set up the plugin's functionality.

The "run" method returns a Result object with two properties port and value.
The value of the port is the result of executing the plugin. The port describes  the output port  of the plugin in the workflow. 
The description of the port and its value can be found in the metadata.documentation.outputs section. 

## Code parts examples to better understand the code and its structure.

Below is a detailed description of the Plugin Object (this is only example), which describes the plugin. It includes an example and comments on its properties to help you
understand its structure:

### Plugin object

```python
Plugin(
    start: bool = False,  # Indicates whether this is the starting node in the workflow
    spec = Spec(
    version='0.8.1', # Plugin version
    module,  # The module containing the plugin's code
    className,  # The class name of the plugin
    inputs=["payload"],  # Input ports
    outputs=["true", "false"],  # Available output ports of the plugin
    init={  # Initial values of the configuration
        "condition": "",
        "trigger_once": False,
        "pass_payload": True,
        "ttl": 0
    },
    form=Form(groups=[  # Describes the configuration form
        FormGroup(
            name="Condition statement",
            fields=[  # Form fields
                FormField(
                    id="condition",  # The ID that matches the configuration key (e.g., "condition" in this example)
                    name="If condition statement",  # Form field for configuring the "condition" key in the init
                    description="Provide a condition for the IF statement. If the condition is met, the payload "
                                "will be returned on the TRUE port; otherwise, the FALSE port is triggered.",
                    # Description of the configuration key. FormComponent.type describes the form field type used to imput data. 
                    component=FormComponent(type="textarea", props={"label": "condition"})
                ),
                ...
            ]
        ),
    ]),
),
                         metadata = MetaData(
    name='If',  # The name of the plugin
    desc='This is a conditional action that selectively runs a branch of the workflow.',
    # A brief description of the plugin
    documentation=Documentation(  # Documentation of plugin ports
        inputs={  # Input port
            "payload": PortDoc(desc="This port accepts a payload object.")
        },
        outputs={  # Output ports
            "true": PortDoc(desc="Returns the payload if the defined condition is met."),
            "false": PortDoc(desc="Returns the payload if the defined condition is NOT met.")
        }
    )
)
)
```

### Loading resources

If you see the code:

```python
resource = await resource_db.load(self.config.resource.id)
self.credentials = resource.credentials.get_credentials(self, output="Here is the resource type")
```

It is also may be represented in form:

Example form field:
```python
FormField(
    id="resource",
    name="Resource",
    description="Resource description",
    component=FormComponent(type="resource", props={"label": "Here is the resource type", "tag": "twilio"})
)
```
Mention it in the documentation. 

Please use the above information to create clear and understandable documentation for the Tracardi plugin.


### Dot parser

If you see the code that does this:

```python
# Get DotAccessor
dot = self._get_dot_accessor(payload)
# Lets assume that self.config.some-configuration = "event@path.to.property". 
# It replace doted notation ("event@path.to.property") with value form event that is in path.to.property
# And assigns it to value variable. 
value = dot[self.config.some-configuration]
```

It means that it parses `some-propery` from the configuration (which is usually the dictionary) and replaces the dot notated values that reference the internet data of workflow. 



If you see the code that does this:

```python
# Get DotAccessor
dot = self._get_dot_accessor(payload)
# Get traverser that goes through the dict and finds doted notation like this "key": "event@path.to.property"
converter = DictTraverser(dot)
# Replace "event@path.to.property" with value form event that is in path.to.property
converter.reshape(self.config.some-property)
```

It means that it parses `some-propery` from the configuration (which is usually the dictionary) and replaces the dot notated values that reference the internet data of workflow. 


# Operations inside the run method

If the plugin updates the execution graph it means it updates workflow so event, profile, or session is available as internal state of workflow.

# Documentation template

Use this template to generate the documentation:


```markdown
# <Put here plugin name from metadata.name>

<Put here plugin short description inferred from the code and available manual.></Put>

# Version

<Put the version of the plugin the documentation was created for. Plugin version can be found in code in `spec.version` property of Plugin object.>

## Description

<Put here verbose description of plugin. Use the logic from the run method to describe how the plugin works. Describe it setp by step. If possible include in here the example of the output from the plugin.> 


# Inputs and Outputs

<Put here information about input and outputs with examples. Put if possible exmples in JSON format of input and output values. Mention if the plugin can start the workflow.>


# Configuration

<Put here the configuration description in a bullet like style with all configuration parameters.>

# JSON Configuration

<Put here the data from spec.init filled with some example values. Only one example.>

# Required resources

<Put here required resources. If none recourse defined in the plugin form or code write "This plugin does not require external resources tobe configured".>

# Errors

<Put here all possible errors. Put here Exception message (not exception type) theat means if there is ` raise ValueError("Profile event sequencing can not be performed without profile. Is this a profile less event?")` "Profile event sequencing can not be performed without profile. Is this a profile less event?" not `ValueError`.
and after the error the description when it may occur.>

```

# What are the limitation of MD markup in the response

There is only one, do not use `` in the response. So `some text` is not allowed. If you to stress some text use __some text__ instead.

---
Here is the full plugin code:

```python
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.domain.config import PluginConfig
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent, \
    PortDoc, Documentation


class Configuration(PluginConfig):
    set1: str
    set2: str
    operation: str


def validate(config: dict):
    return Configuration(**config)


class SetOperationPlugin(ActionRunner):
    config: Configuration

    async def set_up(self, config):
        self.config = validate(config)

    async def run(self, payload, in_edge=None):
        dot = self._get_dot_accessor(payload)
        set1 = set(dot[self.config.set1])
        set2 = set(dot[self.config.set2])

        operation = self.config.operation.lower()

        try:
            if operation == "intersection":
                result_set = list(set1.intersection(set2))
            elif operation == "union":
                result_set = list(set1.union(set2))
            elif operation == "difference":
                result_set = list(set1.difference(set2))
            elif operation == "symmetric_difference":
                result_set = list(set1.symmetric_difference(set2))
            elif operation == "is_subset":
                result_set = set1.issubset(set2)
            elif operation == "is_superset":
                result_set = set1.issuperset(set2)
            else:
                raise ValueError("Invalid operation specified.")

            return Result(port="result", value={"result": result_set})

        except Exception as e:
            return Result(port="error", value={"message": str(e)})


def register() -> Plugin:
    return Plugin(
        spec=Spec(
            module=__name__,
            className=SetOperationPlugin.__name__,
            init={
                "set1": "",
                "set2": "",
                "operation": "intersection"
            },
            form=Form(groups=[
                FormGroup(
                    name="Plugin Configuration",
                    fields=[
                        FormField(
                            id="set1",
                            name="Set 1",
                            description="Reference to the first set data.",
                            component=FormComponent(type="dotPath", props={"label": "Set 1"})
                        ),
                        FormField(
                            id="set2",
                            name="Set 2",
                            description="Reference to the second set data.",
                            component=FormComponent(type="dotPath", props={"label": "Set 2"})
                        ),
                        FormField(
                            id="operation",
                            name="Set Operation",
                            description="Select the set operation to perform.",
                            component=FormComponent(type="select", props={
                                "label": "Set Operation",
                                "items": {
                                    "intersection": "Intersection",
                                    "union": "Union",
                                    "difference": "Difference",
                                    "symmetric_difference": "Symmetric Difference",
                                    "is_subset": "Is Subset",
                                    "is_superset": "Is Superset"
                                }
                            })
                        )
                    ]
                ),
            ]),
            inputs=['payload'],
            outputs=["result", "error"],
            version='8.2.0',
            license="MIT + CC",
            author="Risto Kowaczewski"
        ),
        metadata=MetaData(
            name="Set Operation Plugin",
            desc='Perform set operations on two sets of data.',
            group=["Data Processing"],
            documentation=Documentation(
                inputs={"payload": PortDoc(desc="Input payload.")},
                outputs={
                    "result": PortDoc(desc="Result of the set operation."),
                    "error": PortDoc(desc="Error message if an exception occurs.")
                }
            )
        )
    )
```


Available manual:

The plugin use and operation definition and two sets. Sets data can be referenced from the internal state of workflow. 
Usually the value is as list so convert them to sets. Then use the operation that can be:

Intersection: To find the common elements between two sets, you can use the intersection() method or the & operator. For example, if you have two sets, set1 and set2, you can find their intersection as intersection_set = set1.intersection(set2) or intersection_set = set1 & set2.

Union: To find the combined set of unique elements from two sets, you can use the union() method or the | operator. For example, if you have two sets, set1 and set2, you can find their union as union_set = set1.union(set2) or union_set = set1 | set2.

Difference: To find the elements that exist in one set but not in another, you can use the difference() method or the - operator. For example, if you have two sets, set1 and set2, you can find the elements that are in set1 but not in set2 as difference_set = set1.difference(set2) or difference_set = set1 - set2.

Symmetric Difference: To find the elements that exist in either of the sets but not in both, you can use the symmetric_difference() method or the ^ operator. For example, if you have two sets, set1 and set2, you can find the symmetric difference as symmetric_difference_set = set1.symmetric_difference(set2) or symmetric_difference_set = set1 ^ set2.

Subset Check: You can check if one set is a subset of another using the issubset() method or the <= operator. For example, if you have two sets, set1 and set2, you can check if set1 is a subset of set2 as is_subset = set1.issubset(set2) or is_subset = set1 <= set2.

Superset Check: You can check if one set is a superset of another using the issuperset() method or the >= operator. For example, if you have two sets, set1 and set2, you can check if set1 is a superset of set2 as is_superset = set1.issuperset(set2) or is_superset = set1 >= set2.

and calculate the result. Then return the result on the port named `result`. If there is an error
return its message on the error port.

Include all necessary classes and functions like Configuration, registration, validation, etc in one file.
Plugin must return data only on ports. Do not write any explanation just code.

