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
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.runner import ActionRunner
from .model.config import Config
from tracardi.service.plugin.domain.result import Result
from tracardi.service.storage.driver.elastic import consent_type as consent_type_db
from tracardi.domain.consent_type import ConsentType


def validate(config: dict) -> Config:
    return Config(**config)


class RequireConsentsAction(ActionRunner):

    config: Config

    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None) -> Result:
        if self.event.metadata.profile_less is True:
            self.console.warning("Cannot perform consent check on profile less event.")
            return Result(port="false", value=payload)

        consent_ids = [consent["id"] for consent in self.config.consent_ids]

        profile_consents_copy = self.profile.consents
        for consent_id in profile_consents_copy:
            revoke = self.profile.consents[consent_id].revoke
            if revoke is not None and revoke < self.event.metadata.time.insert:
                self.profile.consents.pop(consent_id)

        for consent_id in consent_ids:
            consent_type = await consent_type_db.get_by_id(consent_id)

            if consent_type is None:
                raise ValueError(f"There is no consent type with ID {consent_id}")
            consent_type = ConsentType(**consent_type)

            if self.config.require_all is True:
                if consent_id not in self.profile.consents:
                    return Result(port="false", value=payload)

                if consent_type.revokable is True:

                    if self.profile.consents[consent_id].revoke is None:
                        self.console.warning(f"Consent type {consent_type.name} is set as revokable by "
                                             f"the revoke date is not set for this profile. "
                                             f"I an assuming that this consent is "
                                             f"timeless.")
                        continue

                    try:
                        revoke_timestamp = self.profile.consents[consent_id].revoke.timestamp()
                    except AttributeError:
                        raise ValueError(f"Corrupted data - no revoke date provided for revokable consent "
                                         f"type {consent_id}")

                    if revoke_timestamp <= self.event.metadata.time.insert.timestamp():
                        return Result(port="false", value=payload)

            else:
                if consent_id in self.profile.consents:
                    if consent_type.revokable is False:
                        return Result(port="true", value=payload)

                    if self.profile.consents[consent_id].revoke is None:
                        return Result(port="true", value=payload)

                    try:
                        revoke_timestamp = self.profile.consents[consent_id].revoke.timestamp()
                    except AttributeError as e:
                        raise ValueError(f"Corrupted data - no revoke date provided for revokable consent "
                                         f"type {consent_id}. Reason: {str(e)}")

                    if revoke_timestamp > self.event.metadata.time.insert.timestamp():
                        return Result(port="true", value=payload)

        return Result(port="true" if self.config.require_all is True else "false", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='RequireConsentsAction',
            inputs=["payload"],
            outputs=["true", "false"],
            version='0.6.2',
            license="MIT + CC",
            author="Dawid Kruk",
            manual="require_consents_action",
            form=Form(
                groups=[
                    FormGroup(
                        name="Consent requirements",
                        fields=[
                            FormField(
                                id="consent_ids",
                                name="IDs of required consents",
                                description="Provide a list of IDs of consents that the profile must grant. "
                                            "Press enter to add more the one consent.",
                                component=FormComponent(type="consentTypes")
                            ),
                            FormField(
                                id="require_all",
                                name="Require all",
                                description="If set to ON, plugin will require all of selected consents to be granted "
                                            "and not revoked. If set to OFF, plugin will require only one of defined "
                                            "consents to be granted.",
                                component=FormComponent(type="bool", props={"label": "Require all"})
                            )
                        ]
                    )
                ]
            ),
            init={
                "consent_ids": [],
                "require_all": False
            }
        ),
        metadata=MetaData(
            name='Has consents',
            desc='Checks if defined consents are granted by current profile.',
            icon='consent',
            group=["Consents"],
            type="condNode",
            tags=['condition'],
            purpose=['collection', 'segmentation'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "true": PortDoc(desc="This port returns given payload if defined consents are granted."),
                    "false": PortDoc(desc="This port returns given payload if defined consents are not granted.")
                }
            )
        )
    )

```

```


Available manual:

# Check granted profile consents

This plugin takes in a list of consent ID and checks if current profile has granted
one of them, or all of them.

## Inputs
This plugin takes any payload as input

## Outputs
This plugin outputs given payload on port **true** if required consents are granted,
or on port **false** if required consents are not granted.

## Plugin configuration
#### With form
- IDs of required consents - provide a list of consents that you want to require to
  be granted by the profile.
- Require all - if this switch is set to ON, plugin will require all of provided
  consent types to granted by profile. If it is set to OFF, only one consent has to
  be granted.

#### Advanced configuration
```json
{
  "consent_ids": [
    {
      "id": "<id-of-consent>",
      "name": "<name-of-consent>"
    },
    {
      "id": "<id-of-second-consent>",
      "name": "<name-of-second-consent>"
    },
    "..."
  ],
  "require_all": "<bool>"
}
```
