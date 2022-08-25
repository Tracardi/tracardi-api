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
"""
for module_name, class_name, test_init in _yield_module_class():
    print(module_name, class_name)
    def_code = f"""async def test_should_set_up_plugin_{camel_to_snake(class_name)}():
    module = import_package(\"{module_name}\")
    plugin_class = load_callable(module, \"{class_name}\")
    plugin = plugin_class()
    await plugin.set_up({test_init})
"""
    code = f"{code}\n\n{def_code}"

with open('test_plugin_set_up.py', 'w') as f:
    f.write(code)
