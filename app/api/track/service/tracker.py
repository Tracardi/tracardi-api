import asyncio
import logging
from typing import List

from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult

from tracardi.domain.console import Console

from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from app.api.track.service.merging import merge
from app.api.track.service.segmentation import segment
from tracardi.domain.session import Session
from tracardi.domain.value_object.tracker_payload_result import TrackerPayloadResult
from tracardi.config import tracardi
from tracardi.process_engine.rules_engine import RulesEngine
from tracardi.domain.value_object.collect_result import CollectResult
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.service.storage.factory import StorageFor, StorageForBulk
from tracardi.service.storage.helpers.debug_saver import save_debug_info
from tracardi.service.storage.helpers.flow_loader import load_flow
from tracardi.service.storage.helpers.profile_loader import load_merged_profile
from tracardi.service.storage.helpers.rules_loader import load_rules
from tracardi.service.storage.helpers.segment_loader import load_segment_by_event_type
from tracardi.service.storage.helpers.source_cacher import source_cache
from tracardi.service.storage.helpers.events_saver import save_events
from tracardi.service.storage.helpers.profile_saver import save_profile
from tracardi.service.storage.helpers.session_saver import save_session

logger = logging.getLogger('app.api.track.service.tracker')


async def _persist(session: Session, events: List[Event],
                   tracker_payload: TrackerPayload, profile: Profile = None) -> CollectResult:
    # Save profile
    if profile.operation.new:
        save_profile_result = await save_profile(profile)
    else:
        save_profile_result = BulkInsertResult()

    # Save session
    persist_session = False if tracker_payload.is_disabled('saveSession') else True
    save_session_result = await save_session(session, profile, persist_session)

    # Save events
    persist_events = False if tracker_payload.is_disabled('saveEvents') else True
    save_events_result = await save_events(events, persist_events)

    return CollectResult(
        session=save_session_result,
        profile=save_profile_result,
        events=save_events_result
    )


async def track_event(tracker_payload: TrackerPayload, ip: str):
    tracker_payload.metadata.ip = ip
    source = await source_cache.validate_source(source_id=tracker_payload.source.id)

    # Get session
    if tracker_payload.session.id is None:
        raise ValueError("Session must be set.")

    # Load session from storage
    session = await StorageFor(tracker_payload.session).index("session").load(Session)  # type: Session

    # Get profile
    profile, session = await tracker_payload.get_profile_and_session(session, load_merged_profile)

    # Get events
    events = tracker_payload.get_events(session, profile)

    debug_info_by_event_type_and_rule_name = None
    segmentation_result = None

    console_log = []
    rules_engine = RulesEngine(
        session,
        profile,
        events_rules=load_rules(events),
        console_log=console_log
    )

    try:

        # Invoke rules engine
        debug_info_by_event_type_and_rule_name, ran_event_types, console_log = await rules_engine.invoke(
            load_flow,
            tracker_payload.source.id)

        # Segment
        segmentation_result = await segment(rules_engine.profile, ran_event_types, load_segment_by_event_type)

    except Exception as e:
        message = 'Rules engine or segmentation returned an error `{}`'.format(str(e))
        console_log.append(
            Console(
                profile_id=rules_engine.profile.id,
                origin='profile',
                class_name='RulesEngine',
                module='tracker',
                type='error',
                message=message
            )
        )
        logger.error(message)

    save_tasks = []
    try:
        # Merge
        profiles_to_disable = await merge(rules_engine.profile, limit=2000)
        if profiles_to_disable is not None:
            task = asyncio.create_task(
                StorageForBulk(profiles_to_disable).index('profile').save())
            save_tasks.append(task)
    except Exception as e:
        message = 'Profile merging returned an error `{}`'.format(str(e))
        logger.error(message)
        console_log.append(
            Console(
                profile_id=rules_engine.profile.id,
                origin='profile',
                class_name='merge',
                module='app.api.track.service',
                type='error',
                message=message
            )
        )

    # Must be the last operation
    try:
        if rules_engine.profile.operation.needs_update():
            await save_profile(profile)
    except Exception as e:
        message = "Profile update returned an error: `{}`".format(str(e))
        console_log.append(
            Console(
                profile_id=rules_engine.profile.id,
                origin='profile',
                class_name='tracker',
                module='tracker',
                type='error',
                message=message
            )
        )
        logger.error(message)

    try:

        # Save debug info
        save_tasks.append(asyncio.create_task(save_debug_info(debug_info_by_event_type_and_rule_name)))

        # Run tasks
        await asyncio.gather(*save_tasks)

    except Exception as e:
        message = "Error during debug info or disabling profiles.: `{}`".format(str(e))
        logger.error(message)
        console_log.append(
            Console(
                profile_id=rules_engine.profile.id,
                origin='profile',
                class_name='tracker',
                module='tracker',
                type='error',
                message=message
            )
        )

    finally:
        # todo maybe persisting profile is not necessary - it is persisted right after workflow - see above
        # TODO notice that profile is saved only when it's new change it when it need update
        # Save profile, session, events
        collect_result = await _persist(session, events, tracker_payload, profile)

        # Save console log
        if console_log:
            save_tasks.append(asyncio.create_task(StorageForBulk(console_log).index('console-log').save()))

    # Prepare response
    result = {}

    # Debugging
    # todo save result to different index
    if not tracardi.track_debug and not tracker_payload.is_disabled('debugger'):
        debug_result = TrackerPayloadResult(**collect_result.dict())
        debug_result = debug_result.dict()
        debug_result['execution'] = debug_info_by_event_type_and_rule_name
        debug_result['segmentation'] = segmentation_result
        debug_result['logs'] = console_log
        result['debugging'] = debug_result

    # Add profile to response
    if tracker_payload.return_profile():
        result["profile"] = profile.dict(
            exclude={
                "traits": {"private": ...},
                "pii": ...,
                "operation": ...
            })
    else:
        result["profile"] = profile.dict(include={"id": ...})

    # Add source to response
    result['source'] = source.dict(include={"consent": ...})

    return result
