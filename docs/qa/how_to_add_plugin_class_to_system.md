# How to add action plugin class to the system?

To register a plugin in Tracardi, follow these steps:

1. **Create the Register Function**: Define a `register` function in the same file where your plugin class is defined.
   This function will return a `Plugin` object containing the specifications and metadata of your plugin.

2 **Specify Plugin Details in Register Function**:

- **Start**: Set to `False` as most plugins do not start the workflow.
- **Spec**: Include details like the module, class name, inputs, outputs, version, license, and author. Example:

```python
spec = Spec(
    module=__name__,
    className='MyPlugin',
    inputs=["payload"],
    outputs=["MyEvent", "NotMyEvent"],
    version='0.1',
    license="MIT",
    author="Your Name"
)
```

- **Metadata**: Define the metadata of the plugin like its name, description, and the group it belongs to. Example:

```python
metadata = MetaData(
    name="My first plugin",
    desc='Descriptive text about what the plugin does.',
    group=["Test plugin"]
)
```

- Please see some already implemented classes in the system to see all the options od register function.

4. **Automatic Plugin Loading**:
    - Navigate to the directory: `/tracardi/service/setup`.
    - Locate the `setup_plugins.py` file. This file contains the list of all available plugins in the system.
    - Add an entry for your plugin in the `installed_plugins` dictionary in the `setup_plugins.py` file. The key should
      be the package of the register function, and the value should be an object of type `PluginMetadata`. Example:
      ```python
      "tracardi.process_engine.action.v1.my_plugin_folder.my_plugin": PluginMetadata(
          test=PluginTest(init=None, resource=None)
      )
      ```

5. **Reinstall Plugins**: After adding your plugin to the `setup_plugins.py` file, restart the Tracardi API for the
   changes to take effect. Then, go to `Processing/Workflows` in the Tracardi GUI, open any workflow, and click
   the `Reinstall Plugins` button to load your new plugin. Alternatively, you can go to `Maintenance/Plug-ins` and click
   the `Reinstall Plugins` button.

This process adds your plugin to the list of available plugins in Tracardi, allowing you to use it in workflows.
Remember to test your plugin thoroughly to ensure it works as expected in the Tracardi environment.

## Example

Below is an example of a `register` function for a hypothetical Tracardi plugin. This function is used to register the
plugin in the Tracardi system, specifying its details, configuration, and capabilities.

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData


def register() -> Plugin:
    return Plugin(
        start=False,  # Indicates that the workflow cannot start from this node
        spec=Spec(
            module=__name__,  # The module where the plugin is defined
            className='MyApiPlugin',  # The name of your plugin class
            init={  # Plugin configuration
                "api_url": "",  # Default value for the API URL
                "api_key": ""  # Default value for the API key
            },
            inputs=["payload"],  # List of input ports
            outputs=["output"],  # List of output ports
            version='0.1',  # Version of your plugin
            license="MIT",  # License type
            author="Your Name"  # Author of the plugin
        ),
        metadata=MetaData(
            name="API Connector Plugin",  # Name of the plugin to display in the workflow editor
            desc='Connects to a specified API and retrieves data.',  # Short description of what the plugin does
            group=["Data Processing"]  # Group under which the plugin will be listed
        )
    )
```

In this example:

- The `Plugin` class is instantiated with specific properties.
- The `start` property is set to `False`, meaning this plugin cannot be used as a starting node in a workflow.
- The `Spec` class defines the technical details of the plugin, like its module location (`__name__`), class
  name (`MyApiPlugin`), input and output ports, version, license, and author.
- The `MetaData` class provides descriptive information about the plugin, like its display
  name (`API Connector Plugin`), a short description (`Connects to a specified API and retrieves data.`), and the group
  in which it will be categorized (`Data Processing`).

After defining this function, remember to add your plugin to the `setup_plugins.py` file in the Tracardi system to
complete the registration process.

## Plugin forms

Action plugins may have forms that fill the plugin configuration.

To add a form to the plugin registration, you'll need to include a `Form` object within the `Spec` class. This form will
define the configuration interface for the plugin in the Tracardi GUI, allowing users to input necessary data, like API
endpoints or other settings.

Here's the updated example of the `register` function with a plugin form:

```python
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className='MyApiPlugin',
            init={
                "api_url": "",  # Default value for the API URL
                "api_key": ""  # Default value for the API key
            },
            form=Form(groups=[
                FormGroup(
                    name="API Configuration",
                    description="Configure the API connection details.",
                    fields=[
                        FormField(
                            id="api_url",
                            name="API URL",
                            description="Enter the API endpoint URL.",
                            component=FormComponent(type="text", props={"label": "API URL"})
                        ),
                        FormField(
                            id="api_key",
                            name="API Key",
                            description="Enter your API key.",
                            component=FormComponent(type="text", props={"label": "API Key"})
                        )
                    ]
                )
            ]),
            inputs=["payload"],
            outputs=["output"],
            version='0.1',
            license="MIT",
            author="Your Name"
        ),
        metadata=MetaData(
            name="API Connector Plugin",
            desc='Connects to a specified API and retrieves data.',
            group=["Data Processing"]
        )
    )
```

In this updated version:

- The `init` property inside `Spec` is used to define the default configuration values. Here, it sets the default values
  for `api_url` and `api_key` as empty strings.
- The `form` property is defined to create a user interface for configuring the plugin. It consists of a `Form` with
  a `FormGroup` containing two `FormField` objects.
    - Each `FormField` represents a field in the form. In this example, there are two fields: one for the API URL and
      another for the API key.
    - The `id` of each `FormField` should match the keys defined in the `init` dictionary.
    - The `FormComponent` defines the type of input control (in this case, `text`) and additional properties like
      labels.

By defining this form, you create a user-friendly interface in the Tracardi workflow editor, allowing users to easily
configure your plugin with the necessary API details.