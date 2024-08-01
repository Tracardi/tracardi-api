# Basic code template for tracardi plugin?

To write a plugin in Tracardi, you typically follow a certain pattern in your Python code. Here's an example of what a
simple code template for a custom plugin may look like:

```python
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
```

Here's a breakdown of the main components of a plugin:

1. First, import the required modules from the Tracardi package.

2. Then, create a class for your plugin that inherits from `ActionRunner`. This makes your class a plugin, capable of
   being run by Tracardi.

3. The `__init__` method is the initializer for your class. You can do any necessary setup here.

4. `set_up` method is for setting up resources if needed.

5. The `run` method is where the processing of data will happen. This function accepts a payload argument which is a
   dictionary and returns the result of the operation as a `Result` object.

6. The `close` method is for cleaning up, closing connections or any necessary teardown.

Remember, the plugin template above is a basic structure. Depending on your goals, your plugin might have additional
methods or an altered structure.

Note that plugins should b register in the system. Check the documentation on how to register the plugin.

---
This document answers the questions:
- How to write a custom plugin?

# Where should I place plugins in tracardi code?

In Tracardi, you should place your plugins in the `tracardi/process_engine/action/v1` folder. The recommended way to
structure the code for your plugin is to create a folder with the plugin name and place the `plugin.py` file inside it.

Here's an example of how you can organize your plugin files:

1. Create a folder with your plugin name. For example, `my_plugin`.

2. Inside the `my_plugin` folder, place the `plugin.py` file. This file will contain the code for your plugin.

The file structure would look like this:

```
tracardi/
└── process_engine/
    └── action/
        └── v1/
            └── my_plugin/
                └── plugin.py
```

By following this structure, you ensure that your plugin is placed in the appropriate directory within the Tracardi
codebase. This makes it easier to manage and maintain your plugins in a standardized manner.

---
This document answers the questions:
- How to write a custom plugin?

# My plugin is not visible on plugin list?

If your plugin is not visible on the plugin list in Tracardi, it is possible that you forgot to register the plugin in
the `tracardi/service/setup/setup_plugins.py` file. To resolve this issue, follow these steps:

1. Open the `setup_plugins.py` file in a text editor.
2. Locate the section where other plugins are registered.
3. Add the following code snippet to register your plugin:

```python
"module-where-the-plugin-code-is-saved": PluginMetadata(
    test=PluginTest(
        init={},  # Here, provide the initialization data for your plugin from the specification
        resource={}  # Here, provide the resource initialization data if it exists
    ),
    plugin_registry="module-where-the-plugin-code-is-saved"
)
```

4. Replace `"module-where-the-plugin-code-is-saved"` with the actual module name or file path where your plugin code is
   saved.
5. Provide the necessary initialization data for your plugin in the `init` and `resource` fields.
6. Save the `setup_plugins.py` file.
7. Restart the Tracardi service for the changes to take effect.
8. After restarting, your plugin should be visible on the plugin list in Tracardi.

By adding the plugin registration code to the `setup_plugins.py` file, you inform Tracardi about the existence of your
plugin and make it accessible through the user interface.

# Give me a fully working example of the tracardi class with description?

Here's the whole code with descriptions for easier understanding:

```python
from pydantic import field_validator
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup, FormComponent, FormField
from tracardi.service.plugin.domain.config import PluginConfig
from password_generator import PasswordGenerator


# Configuration class for the plugin
class Config(PluginConfig):
    max_length: int
    min_length: int
    uppercase: int
    lowercase: int
    special_characters: int

    # Validator to ensure that the minimum length is not greater than the maximum length
    @field_validator("min_length")
    def check_min_max_value(cls, value, values):
        if value > values["max_length"]:
            raise ValueError(
                f"Minimal length {value} cannot be bigger than given maximal length {values['max_length']}")
        return value


# Function to validate the plugin configuration
def validate(config: dict) -> Config:
    return Config(**config)


# Action runner class for the plugin
class PasswordGeneratorAction(ActionRunner):
    config: Config
    pgo: PasswordGenerator

    async def set_up(self, init):
        self.pgo = PasswordGenerator()
        self.config = validate(init)
        self.pgo.minlen = self.config.min_length
        self.pgo.maxlen = self.config.max_length
        self.pgo.minuchars = self.config.uppercase
        self.pgo.minlchars = self.config.lowercase
        self.pgo.minschars = self.config.special_characters

    async def run(self, payload: dict, in_edge=None) -> Result:
        password = self.pgo.generate()
        return Result(port="password", value={"password": password})


# Function to register the plugin
def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='PasswordGeneratorAction',
            inputs=["payload"],
            outputs=["password"],
            version='0.7.1',
            license="MIT",
            author="Mateusz Zitaruk",
            init={
                "min_length": 8,
                "max_length": 13,
                "uppercase": 2,
                "lowercase": 4,
                "special_characters": 2
            },
            manual="password_generator_action",
            form=Form(
                groups=[
                    FormGroup(
                        name="Password generator configuration",
                        fields=[
                            FormField(
                                id="max_length",
                                name="Password maximum length",
                                description="Please provide maximum length of password.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Maximum password length"
                                    }
                                )
                            ),
                            FormField(
                                id="min_length",
                                name="Password minimum length",
                                description="Please provide minimum length of password.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Minimum password length"
                                    }
                                )
                            ),
                            FormField(
                                id="uppercase",
                                name="Uppercase characters",
                                description="Please provide number of uppercase characters.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Number of uppercase letters"
                                    }
                                )
                            ),
                            FormField(
                                id="lowercase",
                                name="Lowercase characters",
                                description="Please provide number of lowercase characters.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Number of lowercase letters"
                                    }
                                )
                            ),
                            FormField(
                                id="special_characters",
                                name="Special characters",
                                description="Please provide number of special characters.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Number of special characters"
                                    }
                                )
                            ),
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Generate password',
            desc='Generate new password according to user input',
            icon='password',
            group=["Operations"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={"password": PortDoc(desc="This port returns generated password.")}
            )
        )
    )
```

This code defines a Tracardi plugin that generates passwords based on user-defined configuration. Here's a breakdown of
the code:

1. Import Statements:

```python
from pydantic import field_validator
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Documentation, PortDoc, Form, FormGroup,
    FormComponent, FormField
from tracardi.service.plugin.domain.config import PluginConfig
from password_generator import PasswordGenerator
```

The import statements bring in the necessary modules and classes for the plugin. These include Pydantic for
configuration validation, Tracardi classes for plugin registration, result handling, and form generation, and the
PasswordGenerator class for generating passwords.

2. Configuration Class:

```python
class Config(PluginConfig):
    max_length: int
    min_length: int
    uppercase: int
    lowercase: int
    special_characters: int

    @field_validator("min_length")
    def check_min_max_value(cls, value, values):
        if value > values["max_length"]:
            raise ValueError(
                f"Minimal length {value} cannot be bigger than given maximal length {values['max_length']}")
        return value
```

The `Config` class defines the plugin configuration using the `PluginConfig` base class. It includes attributes for
maximum length, minimum length, uppercase characters, lowercase characters, and special characters.
The `check_min_max_value` method is a validator that ensures the minimum length is not greater than the maximum length.

3. Configuration Validation Function:

```python
def validate(config: dict) -> Config:
    return Config(**config)
```

The `validate` function takes a dictionary representing the plugin configuration and returns an instance of the `Config`
class after validating the values.

4. Action Runner Class:

```python
class PasswordGeneratorAction(ActionRunner):
    config: Config
    pgo: PasswordGenerator

    async def set_up(self, init):
        self.pgo = PasswordGenerator()
        self.config = validate(init)
        self.pgo.minlen = self.config.min_length
        self.pgo.maxlen = self.config.max_length
        self.pgo.minuchars = self.config.uppercase
        self.pgo.minlchars = self.config.lowercase
        self.pgo.minschars = self.config.special_characters

    async def run(self, payload: dict, in_edge=None) -> Result:
        password = self.pgo.generate()
        return Result(port="password", value={"password": password})
```

The `PasswordGeneratorAction` class is the action runner for the plugin. It inherits from the `ActionRunner` class
provided by Tracardi. It has two main methods:

- The `set_up` method is called during the setup phase of the action and initializes the password generator with the
  provided configuration.
- The `run` method is called when the action is triggered. It generates a password using the configured parameters and
  returns the result.

5. Plugin Registration Function:

```python
def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='PasswordGeneratorAction',
            inputs=["payload"],
            outputs=["password"],
            version='0.7.1',
            license="MIT",
            author="Mateusz Zitaruk",
            init={
                "min_length": 8,
                "max_length": 13,
                "uppercase": 2,
                "lowercase": 4,
                "special_characters": 2
            },
            manual="password_generator_action",
            form=Form(
                groups=[
                    FormGroup(
                        name="Password generator configuration",
                        fields=[
                            FormField(
                                id="max_length",
                                name="Password maximum length",
                                description="Please provide maximum length of password.",
                                component=FormComponent(
                                    type="text",
                                    props={
                                        "label": "Maximum password length"
                                    }
                                )
                            ),
                            # Other form fields...
                        ]
                    )
                ]
            )
        ),
        metadata=MetaData(
            name='Generate password',
            desc='Generate new password according to user input',
            icon='password',
            group=["Operations"],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={"password": PortDoc(desc="This port returns generated password.")}
            )
        )
    )
```

The `register` function returns a `Plugin` instance that represents the plugin registration information. It includes:

- Plugin specifications such as the module and class name, input and output ports, version, license, author information,
  initialization values, and a manual reference.
- Form configuration that defines the user interface for configuring the plugin. It includes form groups, form fields,
  and their respective properties such as labels and descriptions.
- Metadata information such as the plugin name, description, icon, group, and documentation details including inputs and
  outputs descriptions.

By using this code template, you can create your own Tracardi plugins that generate passwords or perform other custom
actions with configurable settings.

---
This document answers the questions:
- How to write a custom plugin?