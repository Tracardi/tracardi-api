from tracardi.domain.event_payload_validator import EventPayloadValidator
from tracardi.service.event_validator import validate
from tracardi.service.notation.dot_accessor import DotAccessor


def test_should_read_the_whole_object():
    dot = DotAccessor(payload={"test": 1})
    validator = EventPayloadValidator(
        validation={"payload@...": {"type": "object"}},
        event_type="page-view",
        name="test",
        enabled=True
    )

    # try:
    validate(dot, validator)
    # except Exception:
    #     assert False


def test_should_read_the_part_of_object():
    dot = DotAccessor(payload={"test": 1})
    validator = EventPayloadValidator(
        validation={"payload@test": {"type": "integer"}},
        event_type="page-view",
        name="test",
        enabled=True
    )

    try:
        validate(dot, validator)
    except Exception:
        assert False
