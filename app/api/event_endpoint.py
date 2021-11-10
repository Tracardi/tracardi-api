from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk, storage_manager
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi_graph_runner.domain.debug_info import DebugInfo
from .auth.authentication import get_current_user
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from .domain.schedule import ScheduleData
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


def __format_time_buckets(row):
    for key, value in row.items():
        timestamp = datetime.fromisoformat(key.replace('Z', '+00:00'))
        # todo timestamp no timezone
        yield {
            "date": "{}".format(timestamp.strftime("%Y/%m/%d")),
            "count": value
        }


@router.get("/events/heatmap/profile/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap_by_profile(id: str):
    try:

        bucket_name = "items_over_time"

        result = await storage.driver.event.heatmap_by_profile(id, bucket_name)
        return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/heatmap", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap():
    try:

        bucket_name = "items_over_time"

        result = await storage.driver.event.heatmap_by_profile(None, bucket_name)
        return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/metadata/type", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types():
    result = await StorageForBulk().index('event').uniq_field_value("type")
    return {
        "total": result.total,
        "result": list(result)
    }


@router.get("/events/by_type/profile/{profile_id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(profile_id: str):
    return await storage.driver.event.aggregate_profile_events_by_type(profile_id, bucket_name='by_type')


@router.get("/events/heatmap_by_profile/profile/{profile_id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(profile_id: str):
    return await storage.driver.event.load_events_heatmap(profile_id)


@router.get("/event/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def get_event(id: str):
    try:
        event = Entity(id=id)
        # Loads TrackerPayload as it has broader data
        full_event = await StorageFor(event).index("event").load(Event)  # type: Event
        if full_event is None:
            raise HTTPException(detail="Event {} does not exist.".format(id), status_code=404)

        profile = Entity(id=full_event.profile.id)
        full_event.profile = await StorageFor(profile).index("profile").load(Profile)

        # todo move to driver
        query = {
            "query": {
                "match": {
                    "events.ids": id,
                }
            }
        }

        index = storage_manager("stat-log")
        event_result = await index.filter(query)

        return {
            "event": full_event,
            "result": list(event_result)[0] if event_result.total == 1 else None
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/event/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def delete_event(id: str):
    try:
        event = Entity(id=id)
        return await StorageFor(event).index("event").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event/debug/{id}", tags=["event"], response_model=List[DebugInfo],
            include_in_schema=server.expose_gui_api)
async def get_event_debug_info(id: str):
    encoded_debug_records = await storage.driver.debug_info.load_by_event(id)
    if encoded_debug_records is not None:
        debug_info = [EventDebugRecord.decode(record, from_dict=True)
                      for record in encoded_debug_records]  # type: List[DebugInfo]
        return debug_info
    return None


@router.get("/event/logs/{id}", tags=["event"], response_model=list, include_in_schema=server.expose_gui_api)
async def get_event_logs(id: str):
    log_records = await storage.driver.console_log.load_by_event(id)
    return list(log_records)


@router.post("/event/schedule", tags=["event"], include_in_schema=server.expose_gui_api)
async def add_scheduled_event(schedule_data: ScheduleData):
    result = await storage.driver.task.create(
        timestamp=schedule_data.schedule.get_parsed_time(),
        type=schedule_data.event.type,
        properties=schedule_data.event.properties,
        context=schedule_data.context.id if schedule_data.context is not None else None,
        session_id=schedule_data.session.id if schedule_data.session is not None else None,
        source_id=schedule_data.source.id,
        profile_id=schedule_data.profile.id,
        status=None
    )
    return {"result": result}
