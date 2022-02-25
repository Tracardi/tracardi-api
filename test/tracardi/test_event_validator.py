from tracardi.domain.event_payload_validator import EventPayloadValidator
from tracardi.service.event_validator import validate
from tracardi.service.notation.dot_accessor import DotAccessor
from tracardi.exceptions.exception import EventValidationException


def test_should_read_the_whole_object():
    dot = DotAccessor(payload={"test": 1})
    validator = EventPayloadValidator(
        validation={"payload@...": {"type": "object"}},
        event_type="page-view",
        name="test",
        enabled=True
    )

    try:
        validate(dot, validator)
    except Exception:
        assert False


def test_should_read_the_part_of_object():
    dot = DotAccessor(payload={"test": {"a": 1}})
    validator = EventPayloadValidator(
        validation={"payload@test": {"type": "object"}},
        event_type="page-view",
        name="test",
        enabled=True
    )

    try:
        validate(dot, validator)
    except Exception:
        assert False


def test_should_differentiate_types():
    dot = DotAccessor(payload={"list": ["a", "b", "c"]})
    validator = EventPayloadValidator(
        validation={"payload@list": {"type": "array"}},
        event_type="page-view",
        name="test",
        enabled=True
    )

    try:
        validate(dot, validator)
    except Exception:
        assert False

    dot = DotAccessor(payload={"list": "not_a_list_for_sure"})

    try:
        validate(dot, validator)
    except EventValidationException:
        assert True


def test_should_not_pass_due_to_invalid_schema():
    dot = DotAccessor(payload={"list": ["a", "b", "c"]})
    validator = EventPayloadValidator(
        validation={
            "email": {
                "type": "string"
            }
        },
        event_type="page-view",
        name="test",
        enabled=True
    )

    try:
        validate(dot, validator)
        assert False
    except EventValidationException:
        assert True
