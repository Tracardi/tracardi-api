import pytest

from tracardi.process_engine.action.v1.contains_string_action import ContainsStringAction, Config
from tracardi.service.plugin.service.plugin_runner import run_plugin


def test_should_return_true():
    init = {
        "field": "payload@field",
        "prefix": "contains"
    }

    payload = {"field": "Test to check if field contains string"}

    result = run_plugin(ContainsStringAction, init, payload)
    assert result.output.port == "true"
    assert result.output.value == {"field": "Test to check if field contains string"}


def test_should_return_false():
    init = {
        "field": "payload@field",
        "prefix": "test"
    }

    payload = {"field": "Test to check if field dont contains string"}

    result = run_plugin(ContainsStringAction, init, payload)
    assert result.output.port == "false"
    assert result.output.value == {"field": "Test to check if field dont contains string"}


def test_empty_prefix_validation():
    with pytest.raises(ValueError):
        Config(field="payload@name", prefix="")