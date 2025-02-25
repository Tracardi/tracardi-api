from typing import Optional

from datetime import datetime
from fastapi import APIRouter, Depends, Response
from tracardi.domain.enum.time_span import TimeSpan
from tracardi.domain.event import Event
from tracardi.domain.storage_results import StorageResults
from tracardi.service import events
from tracardi.service.dependency.adapters.big_data_adapter import *
from tracardi.service.events import get_default_event_type_schema
from app.api.auth.permissions import Permissions

from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


def __format_time_buckets(row):
    for key, value in row.items():
        timestamp = datetime.fromisoformat(key.replace('Z', '+00:00'))
        # todo timestamp no timezone
        yield {
            "date": "{}".format(timestamp.strftime("%Y/%m/%d")),
            "count": value
        }


@router.get("/events/refresh", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def events_refresh_index():
    """
    Refreshes event index.
    """
    return await bd_event_adapter.refresh('event')


@router.get("/events/flush", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def events_flush_index():
    """
    Flushes event index.
    """
    return await bd_event_adapter.flush('event')


@router.get("/event/count", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def count_events():
    return await bd_event_adapter.count()


@router.get("/event/avg/requests", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def average_events():
    return await bd_event_adapter.load_events_avg_requests()


@router.get("/event/avg/process-time", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def count_avg_process_time() -> dict:
    return await bd_event_adapter.load_event_avg_process_time()


@router.get("/events/metadata/type", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def event_types(limit: int = 1000):
    """
    Returns event types
    """
    return await events.get_event_types(limit)


@router.get("/events/by_type", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_types():
    """
    Returns number of events grouped by type
    """
    return await bd_event_adapter.aggregate_event_types_from_db()


@router.get("/events/by_tag", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_tags():
    """
    Returns number of events grouped by tags
    """
    return await bd_event_adapter.aggregate_event_tags_from_db()

# Currently not used
@router.get("/events/by_status", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_statuses():
    """
    Returns number of events grouped by tags
    """
    return await bd_event_adapter.aggregate_event_statuses_from_db()


@router.get("/events/by_device_geo", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_device_geo_location():
    """
    Returns number of events grouped by device location
    """
    return await bd_event_adapter.aggregate_event_devices_geo_from_db()

# Currently not used
@router.get("/events/by_os_name", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_device_by_os():
    """
    Returns number of events grouped by operation system name
    """
    return await bd_event_adapter.aggregate_event_os_names_from_db()


@router.get("/events/by_channel", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_channels():
    """
    Returns number of events grouped by channels
    """
    return await bd_event_adapter.aggregate_event_channels_from_db()


@router.get("/events/by_resolution", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_resolution():
    """
    Returns number of events grouped by screen resolution
    """
    return await bd_event_adapter.aggregate_event_resolutions_from_db()


@router.get("/event/{id}",
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def get_event(id: str, response: Response):
    """
    Returns event with given ID
    """
    record: Optional[Event] = await bd_event_adapter.load_event_from_db(id)

    if record is None:
        response.status_code = 404
        return None

    result = {
        "event": record
    }

    if record.has_meta_data():
        result["_metadata"] = record.get_meta_data()

    return result


@router.delete("/event/{id}", tags=["event"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               include_in_schema=tracardi.expose_gui_api)
async def delete_event(id: str):
    """
    Deletes event with given ID
    """
    return await bd_event_adapter.delete_event_from_db(id)


@router.get("/event/for-source/{source_id}/by-type/{time_span}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_type_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    return await bd_event_adapter.aggregate_events_by_source_and_type(source_id, time_span.value)


@router.get("/event/for-source/{source_id}/by-tag/{time_span}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_tags_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year, EventSourceAnalytics
    """
    return await bd_event_adapter.aggregate_events_by_source_and_tags(source_id, time_span.value)


@router.get("/events/session/{session_id}/profile/{profile_id}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_events_for_session(session_id: str, profile_id: str, limit: int = 20):
    return await bd_event_adapter.load_events_by_session_and_profile(
        profile_id.strip(),
        session_id.strip(),
        limit)


@router.get("/events/profile/{profile_id}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api)
async def get_events_for_profile(profile_id: str, limit: int = 24):
    """ Load events for profile id """

    return await bd_event_adapter.load_events_by_profile_id(
        profile_id,
        limit)


@router.get("/event/type/{event_type}/schema", tags=["event"],
            include_in_schema=tracardi.expose_gui_api)
async def get_event_type_data_schema(event_type: str):
    """Gets pre-defined event type data schema"""

    return get_default_event_type_schema(event_type)
