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

Tracardi plugins are used in workflows. Workflow has internal state. It can be referenced byt the dot notation. In
short, dot notation is a way of referencing data in Tracardi. It is used to access data from the internal state of the
workflow, such as the event, profile, payload, flow, session, and memory. It is written in the form of <source>@<
path.to.data>, where the source is the type of data you are referencing and the path is a string of keys that indicate
where the data is located. Class DotAccessor is used to access dot notated data. Usually the DotAccessor dict is
returned by `self._get_dot_accessor(payload)`. DotAccessor extends dict and acts as dict.

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
                    # Description of the configuration key
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
dot = self._get_dot_accessor(payload)
converter = DictTraverser(dot)
converter.reshape(self.config.some-property)
```

It means that it parses `some-propery` from the configuration (which is usually the dictionary) and replaces the dot notated values that reference the internet data of workflow. 

# Documentation template

Use this template to generate the documentation:


```markdown
# Plugin name

Put here plugin short description inferred from the code and available manual.


## Description

Put here verbose description of plugin. Use the logic from the run method to describe how the plugin works. Describe it setp by step. If possible include in here the example of the output from the plugin. 
Mention the version of the plugin the documentation was created for.

# Inputs and Outputs

Put here information about input and outputs with examples if possible.


# Configuration

Put here the configuration description in a bullet like style with all configuration parameters.

# JSON Configuration

Put here the data from spec.init filled with some example values. Only one example.

# Required resources

Put here required resources. If none recourse defined in the plugin form or code write "This plugin does not require external resources tobe configured".

# Errors

Put here all possible errors. Put here Exception message (not exception type) theat means if there is ` raise ValueError("Profile event sequencing can not be performed without profile. Is this a profile less event?")` "Profile event sequencing can not be performed without profile. Is this a profile less event?" not `ValueError`.
and after the error the description when it may occur.

```

---
Here is the full plugin code:

from tracardi.service.storage.driver.elastic import event as event_db
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from pytimeparse import parse
from .model.configuration import Configuration


def validate(config: dict) -> Configuration:
    return Configuration(**config)


class EventCounter(ActionRunner):
    config: Configuration

    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None) -> Result:
        time_span_in_sec = parse(self.config.time_span.strip("-"))

        no_of_events = await event_db.count_events_by_type(
            self.profile.id,
            self.config.event_type.id,
            time_span_in_sec
        )
        return Result(port="payload", value={"events": no_of_events})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=EventCounter.__name__,
            inputs=["payload"],
            outputs=['payload'],
            version='0.8.1',
            license="MIT",
            author="Dawid Kruk",
            manual="event_counter_action",
            init={
                "event_type": {"name": "", "id": ""},
                "time_span": "-15m"
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="Event counter settings",
                        description="Event counter reads how many events of defined type were triggered "
                                    "within defined time.",
                        fields=[
                            FormField(
                                id="event_type",
                                name="Event type",
                                description="Select event type you would like to count.",
                                component=FormComponent(type="eventType", props={
                                    "label": "Event type"
                                })
                            ),
                            FormField(
                                id="time_span",
                                name="Time span",
                                description="Type time span, e.g. -15minutes.",
                                component=FormComponent(type="text", props={
                                    "label": "Time span"
                                })
                            ),
                        ]
                    )
                ])
        ),
        metadata=MetaData(
            name='Event counter',
            desc='This plugin reads how many events of defined type were triggered within defined time.',
            icon='event',
            group=["Events"],
            tags=['pro', 'event'],
            purpose=['collection', 'segmentation'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="Reads payload object.")
                },
                outputs={
                    "payload": PortDoc(desc="Returns number of event of given type.")
                }
            ),
            pro=True
        )
    )




Available manual:

# Limiter plugin

The plugin limits the number of launches to a certain number in a given period of time. It is particularly useful when we would like to protect valuable resources from overloading or limit the triggering of some plugins.
You have to remember that some events maybe triggered very fast and process time of a event may be longer then the time between the event triggers. That may cause the workflow to run server times. Is such case a throttle (limiter) may be used to limit the number of executions.
It works ina a way that stops execution of a workflow branch if some threshold is passed, for example, 10 starts within one minute. The workflow will work until 10 executions are completed and then will throttle the rest of the executions until one minute end (or other defined time range).

# Configuration

In order to properly configure the plugin, we need to know what resource we are protecting and how we identify it. Let's assume that we want to send emails to the specified email address. However, we don't want the system to send more than one email per day. Regardless of the email's message. In this case, the protected resource is email. Therefore, the key that will identify our limiter (throttle) will be the email address. You can define a pair of keys. e.g. if we do not want the customer to accidentally receive an email with the same content twice, we can set the key for the email and the e-mail message.
The order of throttle keys is important, because this is the way the limiter identifies the protected resource.

# Side effects

The limiters placed in different workflows share the same information if they have he same key. That means if we send emails in many workflow and throttle/limit the number executions based on email - execution in one workflow will add up to the limit on the other workflow as well. This is a very powerful feature that can protect resources across all workflows if set properly.
If you want the limiter to work only for one workflow and not across all workflows add workflow id (or custom key) to a limiter key, e.g. workflow.id + email.

# Advanced JSON configuration

Example

```json
{
  "keys": ["workflow@id", "profile@pii.email", "custom-key"],
  "limit": 10
  "ttl": 60
}
```

* __keys__ - keys that identify the throttle. It may reference data from workflow or be a custome keys
* __limit__ - the number of allowed passes within defined time
* __ttl__ - time to live for a throttle. The time period that must pass for the __limit__ to be reset to 0.

# Outputs

* __pass__ - Triggers this port if not limited. Returns input payload.
* __block__ - Triggers this port if executions are limited. Returns input payload.


