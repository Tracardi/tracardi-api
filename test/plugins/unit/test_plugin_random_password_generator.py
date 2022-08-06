from tracardi.process_engine.action.v1.password_generator_action import PasswordGeneratorAction
from tracardi.service.plugin.service.plugin_runner import run_plugin


def test_should_return_password_length():
    init = {"max_length": 14,
            "min_length": 10,
            "uppercase": 5,
            "lowercase": 5,
            "special_characters": 3}

    payload = {}

    result = run_plugin(PasswordGeneratorAction, init, payload)

    assert result.output.port == "password"
    assert (len(result.output.value["password"])) == init["max_length"]
