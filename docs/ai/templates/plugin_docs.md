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

# Event prerequisites

<Put here information if the plugin only works for sync event or for all events. Plugins that are UIX widgets (usually placed in UIX Widgets group) require an event to synchronious and wait for the workflow to finish. All other plugins do not have this requirement.>

# Errors

<Put here all possible errors. Put here Exception message (not exception type) that means if there is ` raise ValueError("Profile event sequencing can not be performed without profile. Is this a profile less event?")` "Profile event sequencing can not be performed without profile. Is this a profile less event?" not `ValueError`.
and after the error the description when it may occur.>

```

# What are the limitation of MD markup in the response

There is only one, do not use `` in the response. So `some text` is not allowed. If you to stress some text use __some text__ instead.

---
Here is the full plugin code:

```python
import json
from pydantic import field_validator
from tracardi.service.plugin.domain.config import PluginConfig
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, \
    FormField, FormComponent
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from tracardi.domain.profile import Profile
from tracardi.service.segmentation.profile_segmentation_services import add_segment_to_profile


class Configuration(PluginConfig):
    interests: str
    segment_mapping: str
    segments_to_apply: str

    @field_validator('interests')
    @classmethod
    def interests_must_not_be_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Interests must not be empty.")
        return value
    
    @field_validator('segment_mapping')
    @classmethod
    def mapping_must_not_be_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Segment Mapping must not be empty.")
        return value
    
    @field_validator('segments_to_apply')
    @classmethod
    def segments_to_apply_must_not_be_empty(cls, value):
        if value.strip() == "" or value.isnumeric() != True:
            raise ValueError("Segments to Apply must not be empty and must be a number.")
        return value
    
def validate(config: dict):
    return Configuration(**config)

class GroupAndRankInterestsAction(ActionRunner):
    
    config: Configuration
    
    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None) -> Result:
        dot = self._get_dot_accessor(payload)
        profile = Profile(**dot.profile)

        # How plugin works.
        # Example of segment_mapping:
        """
        segment_mapping = {
            "segment_name": ["interest1", "interest2", "interest3"] // Adds 
        }
        """

        # This defines how the segment will be built. The above tells create a `segment_name` from the "interest1" and "interest2", and "interest3".
        # For example "apple-fan-boy": ["iphone", "ipad", "imac"]
        # Profile may have interests associated which can be:

        """
        {
        "ipad": 2,
        "iphone": 5,
        "imac": 1
        }
        """

        # based on that interest new segment is computed. It adds all the interest counts and computes segment rank, which will be in this example 8.
        # Then based on the segments_to_apply only the segments that are above the defined threshold will be applied to the profile.

        try:
            segment_mapping = json.loads(dot[self.config.segment_mapping])
            interests = dot[self.config.interests]

            segment_count = {segment: 0 for segment in segment_mapping.keys()}

            for interest, count in interests.items():
                for segment, keywords in segment_mapping.items():
                    if isinstance(keywords, list) and interest.lower() in keywords:
                        segment_count[segment] += count

            ranked_segments = sorted(segment_count.keys(), key=lambda x: segment_count[x], reverse=True)
            try:
                segments_to_apply=int(dot[self.config.segments_to_apply])
            except Exception:
                # If segments to apply not a number
                message = "Segments To Apply must be a number"
                self.console.error(message)
                return Result(value={"message": message}, port="error")

            if segments_to_apply > len(ranked_segments):
                segments_to_apply=len(ranked_segments)

            # Apply segments to profile
            for index in range(0, segments_to_apply):
                profile = add_segment_to_profile(profile, ranked_segments[index])
                
            self.profile.replace(profile)

            return Result(port='result', value={'applied_segments':ranked_segments})
        except Exception as e:
            return Result(value={"message": str(e)}, port="error")            

def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=GroupAndRankInterestsAction.__name__,
            inputs=["payload"],
            outputs=["result", "error"],
            version='0.9.0',
            init={
                "interests": "profile@interests",  # Interests is a path the where the interests are stored.
                "segment_mapping": "",  # See the "Example of segment_mapping" above
                "segments_to_apply": ""
            },
            form=Form(groups=[
                FormGroup(
                    name="Group And Rank Interests configuration",
                    fields=[
                        FormField(
                            id="interests",
                            name="Interests",
                            description="Location of profile interests, usually profile@interests",
                            component=FormComponent(type="dotPath", props={
                                "label": "Interests",
                                "defaultSourceValue": "profile"
                            })
                        ),
                        FormField(
                            id="segment_mapping",
                            name="Segment Mapping",
                            description="Defines how the segment rank is computed based on profile's interests. It maps key which is a segment name to a list of interests that build this segment.",
                            component=FormComponent(type="json", props={
                                "label": "segment_mapping"
                            })
                        ),
                        FormField(
                            id="segments_to_apply",
                            name="Segments To Apply",
                            description="This setting decides which computed segments get added to a profile. For instance, if the limit is set to 5, the sum of the interests must be more than 5",
                            component=FormComponent(type="dotPath", props={
                                "label": "segments_to_apply"
                            })
                        )
                        
                    ])
            ]),
            license="MIT",
            author="Matt Cameron",
            manual="group_and_rank_interests"
        ),
        metadata=MetaData(
            name='Group and Rank Interests',
            desc='Maps interests to profiles and returns matched profiles in order of importance.',
            icon='GroupAndRankInterests',
            group=['Segmentation'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "result": PortDoc(desc="Returns response from GroupAndRankInterests service."),
                    "error": PortDoc(desc="Returns error message if plugin fails.")
                }
            )
        )
    )


```


Additional manual:

Use the comments from code and add examples.