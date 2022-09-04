from typing import Tuple, Union, Iterator

from tracardi.domain.settings import Settings
from tracardi.service.module_loader import load_callable, import_package
from tracardi.service.plugin.domain.register import Plugin
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.setup.domain.plugin_test_template import PluginTestTemplate
from tracardi.service.setup.setup_plugins import installed_plugins, test_plugins


def _load_plugin_registry_metadata(plugin_module) -> Plugin:
    module = import_package(plugin_module)
    plugin = load_callable(module, 'register')

    plugin_registry = plugin()  # type: Union[Plugin, Tuple[Plugin, Settings]]
    if isinstance(plugin_registry, tuple):
        plugin_registry, _ = plugin_registry

    return plugin_registry


def _yield_module_class() -> Iterator[Tuple[str, str, PluginTestTemplate]]:
    for plugin_module, test_template in installed_plugins.items():
        plugin_registry = _load_plugin_registry_metadata(plugin_module)

        yield plugin_registry.spec.module, plugin_registry.spec.className, test_template

    for plugin_module, test_template in test_plugins.items():
        plugin_registry = _load_plugin_registry_metadata(plugin_module)

        yield plugin_registry.spec.module, plugin_registry.spec.className, test_template


def test_should_find_all_plugins_modules():
    for module_name, class_name, _ in _yield_module_class():
        try:
            import_package(module_name)
            assert True
        except ImportError:
            assert False


def test_should_all_plugins_not_fail_on_init():
    for module_name, class_name, _ in _yield_module_class():
        module = import_package(module_name)
        plugin_class = load_callable(module, class_name)

        plugin = plugin_class()
        assert isinstance(plugin, ActionRunner)


async def test_should_set_up_plugin():
    module_name = "tracardi.process_engine.action.v1.traits.copy_trait_action"
    class_name = "CopyTraitAction"
    module = import_package(module_name)
    plugin_class = load_callable(module, class_name)
    registry = _load_plugin_registry_metadata(module_name)  # type: Plugin
    plugin = plugin_class()
    await plugin.set_up(registry.spec.init)
