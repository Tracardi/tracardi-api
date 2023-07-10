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
# <Put here plugin name from metadata.name>

<Put here plugin short description inferred from the code and available manual.></Put>

# Version

<Put the version of the plugin the documentation was created for. Plugin version can be found in code in `spec.version` property of Plugin object.>

## Description

<Put here verbose description of plugin. Use the logic from the run method to describe how the plugin works. Describe it setp by step. If possible include in here the example of the output from the plugin.> 


# Inputs and Outputs

<Put here information about input and outputs with examples if possible.>


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

---
Here is the full plugin code:

from com_tracardi.service.tracker_event_validator import EventsValidationHandler
from tracardi.service.console_log import ConsoleLog
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from pydantic import validator
from typing import Dict, Union
from tracardi.exceptions.exception import EventValidationException
from tracardi.domain.event_validator import EventValidator, ValidationSchema
import jsonschema
import json
from tracardi.service.plugin.domain.config import PluginConfig


class Config(PluginConfig):
    validation_schema: Union[str, Dict[str, Dict]]

    @validator("validation_schema")
    def validate_config_schema(cls, v):
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Given JSON is invalid.")

        for value in v.values():
            try:
                jsonschema.Draft202012Validator.check_schema(value)
            except jsonschema.SchemaError:
                raise ValueError(f"Given validation JSON-schema is invalid.")
        return v


def validate(config: dict) -> Config:
    return Config(**config)


class SchemaValidator(ActionRunner):

    config: Config

    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        payload_validator = EventValidator(
            validation=ValidationSchema(json_schema=self.config.validation_schema),
            event_type="no-type",
            name="validation",
            id="1",
            tags=[]
        )

        try:
            v = EventsValidationHandler(dot, ConsoleLog())
            result = v.validate_with_multiple_schemas([payload_validator])
            if result:
                return Result(port="true", value=payload)
            return Result(port="false", value=payload)
        except EventValidationException:
            return Result(port="error", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='SchemaValidator',
            inputs=["payload"],
            outputs=["true", "false", "error"],
            version='0.7.4',
            license="Tracardi Commercial License",
            author="Dawid Kruk, Risto Kowaczewski",
            manual="validate_with_json_schema_action",
            init={
                "validation_schema": {}
            },
            form=Form(
                groups=[
                    FormGroup(
                        name="JSON Schema Validation Configuration",
                        fields=[
                            FormField(
                                id="validation_schema",
                                name="JSON validation schema",
                                description="Please provide a JSON validation schema that you want to validate data "
                                            "with.",
                                component=FormComponent(type="json", props={"label": "Schema"})
                            )
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='JSON schema validator',
            desc='Validates objects using provided JSON validation schema.',
            icon='ok',
            group=["Validators"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "true": PortDoc(desc="This port returns payload if it passes defined validation."),
                    "false": PortDoc(desc="This port returns payload if it does not pass defined validation."),
                    "error": PortDoc(desc="This port returns payload if it does not pass defined validation "
                                          "due to an error in validation schema.")
                }
            ),
            commercial=True
        )
    )



Available manual:

# Validate with JSON schema plugin

This plugin validates objects using provided JSON schema.

## Input

This plugin takes any payload as input.

## Outputs

This plugin returns payload on port **TRUE** if validation is passed, or payload on port **FALSE** if validation fails.
If the schema is incorrect then the **ERROR** port is triggered. 

#### JSON configuration

```json
{
  "validation_schema": "<validation-object>"
}
```

Example of valid schema to provide in the form field or as a value of **validation_schema**:

```json
{
  "payload@properties.sale": {
    "type": "object",
    "properties": {
      "price": {
        "type": "number"
      },
      "name": {
        "type": "string",
        "maxLength": 15
      }
    }
  },
  "profile@context.timestamp": {
    "type": "integer"
  }
}
```

```json
 {
    "payload@...": {
      "title": "Product",
      "description": "A product from Acme's catalog",
      "type": "object",
      "properties": {
        "productId": {
          "description": "The unique identifier for a product",
          "type": "integer"
        }
      },
      "required": [
        "productId"
      ]
    }
  }
```

