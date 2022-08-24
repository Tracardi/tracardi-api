from typing import Tuple, Union

from tracardi.domain.settings import Settings
from tracardi.service.module_loader import load_callable, import_package
from tracardi.service.plugin.domain.register import Plugin
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.setup.setup_plugins import installed_plugins


def _yield_module_class():
    for plugin_module in installed_plugins:

        module = import_package(plugin_module)
        plugin = load_callable(module, 'register')

        plugin_registry = plugin()  # type: Union[Plugin, Tuple[Plugin, Settings]]
        if isinstance(plugin_registry, tuple):
            plugin_registry, _ = plugin_registry

        yield plugin_module, plugin_registry.spec.className


def test_should_find_all_plugins_modules():
    for module_name, class_name in _yield_module_class():
        try:
            import_package(module_name)
            assert True
        except ImportError:
            assert False


def test_should_all_plugins_not_fail_on_init():
    for module_name, class_name in _yield_module_class():
        print(module_name)
        module = import_package(module_name)
        plugin_class = load_callable(module, class_name)

        plugin = plugin_class()
        assert isinstance(plugin, ActionRunner)
        print(type(plugin))
