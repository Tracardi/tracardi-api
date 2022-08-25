import pprint
import re

from test.api.plugins.test_all_endpoints import _yield_module_class

pattern = re.compile(r'(?<!^)(?=[A-Z])')
printer = pprint.PrettyPrinter(indent=4)


def camel_to_snake(name):
    return pattern.sub('_', name).lower()


code = """
from test.api.plugins.test_all_endpoints import _load_plugin_registry_metadata
from tracardi.service.module_loader import load_callable, import_package
from tracardi.domain.resource import Resource, ResourceCredentials
from tracardi.service.module_loader import load_callable, import_package
from tracardi.service.wf.domain.node import Node
"""
for module_name, class_name, test_template in _yield_module_class():
    print(module_name, class_name)

    if test_template.resource is not None:
        mocker = \
f"""
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.storage.driver.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={test_template.resource},
                test={test_template.resource}
            )
        )
    )
"""
    else:
        mocker = ""

    def_code = f"""async def test_should_set_up_plugin_{camel_to_snake(class_name)}({'mocker' if test_template.resource is not None else ''}):
    {mocker}
    module = import_package(\"{module_name}\")
    plugin_class = load_callable(module, \"{class_name}\")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module=\"{module_name}\", 
                       className=\"{class_name}\")
    await plugin.set_up({test_template.init})
"""
    code = f"{code}\n\n{def_code}"

with open('../test_plugin_set_up.py', 'w') as f:
    f.write(code)
