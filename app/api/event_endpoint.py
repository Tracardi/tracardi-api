from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from tracardi.domain.console import Console
from tracardi.domain.enum.time_span import TimeSpan

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi.service.wf.domain.debug_info import DebugInfo
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from .auth.permissions import Permissions
from .domain.schedule import ScheduleData
from ..config import server
from elasticsearch.exceptions import ElasticsearchException

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


def __format_time_buckets(row):
    for key, value in row.items():
        timestamp = datetime.fromisoformat(key.replace('Z', '+00:00'))
        # todo timestamp no timezone
        yield {
            "date": "{}".format(timestamp.strftime("%Y/%m/%d")),
            "count": value
        }


@router.get("/events/refresh", tags=["event"], include_in_schema=server.expose_gui_api)
async def events_refresh_index():
    """
    Refreshes event index.
    """
    try:
        return await storage.driver.event.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/heatmap/profile/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap_by_profile(id: str):
    """
    Returns events heatmap for profile with given ID
    """
    try:

        bucket_name = "items_over_time"

        result = await storage.driver.event.heatmap_by_profile(id, bucket_name)
        return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/heatmap", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap():
    """
    Returns events heatmap
    """
    try:

        bucket_name = "items_over_time"

        result = await storage.driver.event.heatmap_by_profile(None, bucket_name)
        return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/metadata/type", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(query: str = None, limit: int = 1000):
    """
    Returns event types
    """
    result = await StorageForBulk().index('event').uniq_field_value("type", search=query, limit=limit)
    return {
        "total": result.total,
        "result": list(result)
    }


@router.get("/events/by_type/profile/{profile_id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(profile_id: str):
    """
    Returns number of events grouped by type for profile with given ID
    """
    return await storage.driver.event.aggregate_profile_events_by_type(profile_id, bucket_name='by_type')


@router.get("/events/by_type", tags=["event"], include_in_schema=server.expose_gui_api)
async def aggregate_event_types():
    """
    Returns number of events grouped by type
    """
    return await storage.driver.event.aggregate_event_type()


@router.get("/events/by_tag", tags=["event"], include_in_schema=server.expose_gui_api)
async def aggregate_event_tags():
    """
    Returns number of events grouped by tags
    """
    return await storage.driver.event.aggregate_event_tag()


@router.get("/events/by_source", tags=["event"], include_in_schema=server.expose_gui_api)
async def aggregate_event_tags():
    """
    Returns number of events grouped by event source
    """
    return await storage.driver.event.aggregate_events_by_source()


@router.get("/events/heatmap_by_profile/profile/{profile_id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(profile_id: str):
    """
    Returns events heatmap for profile with given ID
    """
    return await storage.driver.event.load_events_heatmap(profile_id)


@router.get("/events/heatmap", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types():
    """
    Returns number of events grouped by event time
    """
    return await storage.driver.event.load_events_heatmap()


@router.get("/event/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def get_event(id: str):
    """
    Returns event with given ID
    """
    try:
        event = await StorageFor(Entity(id=id)).index("event").load(Event)  # type: Event
        if event is None:
            raise HTTPException(detail="Event {} does not exist.".format(id), status_code=404)

        return {
            "event": event
        }

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/event/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def delete_event(id: str):
    """
    Deletes event with given ID
    """
    try:
        event = Entity(id=id)
        return await StorageFor(event).index("event").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event/debug/{id}", tags=["event"], response_model=List[DebugInfo],
            include_in_schema=server.expose_gui_api)
async def get_event_debug_info(id: str):
    """
    Returns debug info of event with given ID
    """
    encoded_debug_records = await storage.driver.debug_info.load_by_event(id)
    if encoded_debug_records is not None:
        debug_info = [EventDebugRecord.decode(record, from_dict=True)
                      for record in encoded_debug_records]  # type: List[DebugInfo]
        return debug_info
    return None


@router.get("/event/logs/{id}", tags=["event"], response_model=list, include_in_schema=server.expose_gui_api)
async def get_event_logs(id: str):
    """
    Returns event logs for event with given ID
    """
    log_records = await storage.driver.console_log.load_by_event(id)
    return [Console.decode_record(log) for log in log_records]


@router.post("/event/schedule", tags=["event"], include_in_schema=server.expose_gui_api)
async def add_scheduled_event(schedule_data: ScheduleData):
    """
    Adds scheduled event
    """
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


@router.get("/event/group/by_tags/profile/{profile_id}", tags=["event"],
            include_in_schema=server.expose_gui_api, response_model=dict)
async def get_grouped_by_tags_prof(profile_id: str):
    """
    Returns events gruped by tags for profile with given ID
    """
    aggregate_query = {
        "for_tags": {
            "terms": {
                "field": "tags.values"
            }
        },
        "for_missing_tags": {
            "missing": {
                "field": "tags.values"
            }
        }
    }
    try:
        result = await storage.driver.event.aggregate_profile_events(
            profile_id=profile_id,
            aggregate_query=aggregate_query
        )
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


@router.get("/event/group/by_tags/from/{time_from}/to/{time_to}", tags=["event"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_grouped_by_tags_time(time_from: datetime, time_to: datetime):

    """
    Accepted time format: 2021-09-15T15:53:00
    """

    aggregate_query = {
        "for_tags": {
            "terms": {
                "field": "tags.values"
            }
        },
        "for_missing_tags": {
            "missing": {
                "field": "tags.values"
            }
        }
    }
    try:
        result = await storage.driver.event.aggregate_timespan_events(
            time_from=time_from,
            time_to=time_to,
            aggregate_query=aggregate_query
        )
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


@router.get("/event/for-source/{source_id}/by-type/{time_span}", tags=["event"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_type_time(source_id: str, time_span: TimeSpan):

    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    try:
        return await storage.driver.event.aggregate_source_by_type(source_id, time_span)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event/for-source/{source_id}/by-tag/{time_span}", tags=["event"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_tags_time(source_id: str, time_span: TimeSpan):

    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    try:
        return await storage.driver.event.aggregate_source_by_tags(source_id, time_span)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
