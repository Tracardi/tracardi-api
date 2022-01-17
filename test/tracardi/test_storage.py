from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi.domain.segment import Segment
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.type import Type
from tracardi.domain.rule import Rule
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.flow.start.start_action import StartAction, register
from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.flow import Flow
from tracardi.domain.profile import Profile
from tracardi.domain.resource import ResourceRecord
from tracardi.domain.session import Session, SessionMetadata
from tracardi.service.storage.factory import StorageFor
from tracardi.service.wf.service.builders import action


async def test_storage(event_loop):
    print(event_loop)
    # Create flow

    debug = action(DebugPayloadAction, {
        "event": {
            "type": "test",
        }
    })

    start = action(StartAction)
    increase_views = action(IncreaseViewsAction)
    end = action(EndAction)

    flow = Flow.build("End2End - flow", id="flow-id")
    flow += debug('event') >> start('payload')
    flow += start('payload') >> increase_views('payload')
    flow += increase_views('payload') >> end('payload')
    flow_record = flow.get_production_workflow_record()

    objects = [
        Profile(id="1"),
        Session(id="1", profile=Profile(id="1"), metadata=SessionMetadata()),
        flow_record,
        ResourceRecord(id="2", type="test"),
        Rule(id="1", name="rule",
             event=Type(type="type"),
             source=NamedEntity(id="source-id", name="test source"),
             flow=NamedEntity(id="1", name="flow")),
        Segment(id="1", name="segment", condition="a>1"),  # todo segment needs validation on condition
        EventDebugRecord(id="1", content="abc"),
        FlowActionPluginRecord.encode(FlowActionPlugin(id="2", plugin=register())),
    ]

    for instance in objects:
        db = StorageFor(instance).index()

        result = await db.save()
        assert result.saved == 1

        await db.refresh()

        result = await db.load()

        assert isinstance(result, db.domain_class_ref)

    for instance in objects:
        db = StorageFor(instance).index()
        await db.delete()
