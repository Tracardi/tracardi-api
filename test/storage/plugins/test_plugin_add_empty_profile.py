from tracardi.domain.entity import Entity
from tracardi.domain.event_metadata import EventMetadata, EventTime
from tracardi.domain.session import Session, SessionMetadata
from tracardi.domain.event import Event, EventSession
from tracardi.process_engine.action.v1.internal.add_empty_profile.plugin import AddEmptyProfileAction
from tracardi.service.plugin.service.plugin_runner import run_plugin


def test_plugin_add_empty_profile():
    payload = {}
    event = Event(
        id='1',
        type='text',
        metadata=EventMetadata(time=EventTime(), profile_less=True),
        session=EventSession(id='1'),
        source=Entity(id='1')
    )
    session = Session(
        id='1',
        metadata=SessionMetadata()
    )
    result = run_plugin(AddEmptyProfileAction, {}, payload=payload, event=event, session=session, profile=None)
    assert result.event.metadata.profile_less is False
    assert result.event.profile is not None

