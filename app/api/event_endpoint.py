from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Response
from tracardi.domain.console import Console
from tracardi.domain.enum.time_span import TimeSpan

from tracardi.service.storage.driver import storage
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi.service.wf.domain.debug_info import DebugInfo
from .auth.permissions import Permissions
from ..config import server

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


@router.get("/events/refresh", tags=["event"], include_in_schema=server.expose_gui_api)
async def events_refresh_index():
    """
    Refreshes event index.
    """
    return await storage.driver.event.refresh()


@router.get("/events/flush", tags=["event"], include_in_schema=server.expose_gui_api)
async def events_refresh_index():
    """
    Flushes event index.
    """
    return await storage.driver.event.flush()


@router.get("/event/count", tags=["event"], include_in_schema=server.expose_gui_api)
async def count_events():
    return await storage.driver.event.count()


@router.get("/event/avg/requests", tags=["event"], include_in_schema=server.expose_gui_api)
async def count_events():
    result = await storage.driver.event.count(query={
        "query": {
            "range": {
                "metadata.time.insert": {
                    "gte": "now-5m",
                    "lte": "now"
                }
            }
        }
    })
    return result['count'] / (5 * 60) if 'count' in result else 0


@router.get("/event/avg/process-time", tags=["event"], include_in_schema=server.expose_gui_api)
async def count_avg_process_time() -> dict:
    return await storage.driver.event.get_avg_process_time()


# todo not used - not in tests
@router.get("/events/heatmap/profile/{id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap_by_profile(id: str):
    """
    Returns events heatmap for profile with given ID
    """
    bucket_name = "items_over_time"

    result = await storage.driver.event.heatmap_by_profile(id, bucket_name)
    return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]


# todo not used -  not in tests
@router.get("/events/heatmap", tags=["event"], include_in_schema=server.expose_gui_api)
async def heatmap():
    """
    Returns events heatmap
    """
    bucket_name = "items_over_time"

    result = await storage.driver.event.heatmap_by_profile(None, bucket_name)
    return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]


@router.get("/events/metadata/type", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(query: str = None, limit: int = 1000):
    """
    Returns event types
    """
    result = await storage.driver.event.unique_field_value(query, limit)
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


@router.get("/events/by_status", tags=["event"], include_in_schema=server.expose_gui_api)
async def aggregate_event_statuses():
    """
    Returns number of events grouped by tags
    """
    return await storage.driver.event.aggregate_event_status()


@router.get("/events/by_source", tags=["event"], include_in_schema=server.expose_gui_api)
async def aggregate_event_tags(buckets_size: int = 30):
    """
    Returns number of events grouped by event source
    """
    return await storage.driver.event.aggregate_events_by_source(buckets_size=buckets_size)


# todo not used -  not in tests
@router.get("/events/heatmap_by_profile/profile/{profile_id}", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types(profile_id: str):
    """
    Returns events heatmap for profile with given ID
    """
    return await storage.driver.event.load_events_heatmap(profile_id)


# todo not used -  not in tests
@router.get("/events/heatmap", tags=["event"], include_in_schema=server.expose_gui_api)
async def event_types():
    """
    Returns number of events grouped by event time
    """
    return await storage.driver.event.load_events_heatmap()


@router.get("/event/{id}",
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            tags=["event"], include_in_schema=server.expose_gui_api)
async def get_event(id: str, response: Response):
    """
    Returns event with given ID
    """
    record = await storage.driver.event.load(id)

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
               include_in_schema=server.expose_gui_api)
async def delete_event(id: str):
    """
    Deletes event with given ID
    """
    return await storage.driver.event.delete_by_id(id)


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


# todo not used -  not in tests
@router.get("/event/group/by_tags/profile/{profile_id}", tags=["event"],
            include_in_schema=server.expose_gui_api, response_model=dict)
async def get_grouped_by_tags_profile(profile_id: str):
    """
    Returns events grouped by tags for profile with given ID
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
    result = await storage.driver.event.aggregate_profile_events(
            profile_id=profile_id,
            aggregate_query=aggregate_query
        )
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


# todo not used -  not in tests
@router.get("/event/group/by_tags/from/{time_from}/to/{time_to}", tags=["event"],
            include_in_schema=server.expose_gui_api,
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
    result = await storage.driver.event.aggregate_timespan_events(
            time_from=time_from,
            time_to=time_to,
            aggregate_query=aggregate_query
        )
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


@router.get("/event/for-source/{source_id}/by-type/{time_span}", tags=["event"],
            include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_type_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    return await storage.driver.event.aggregate_source_by_type(source_id, time_span)


@router.get("/event/for-source/{source_id}/by-tag/{time_span}", tags=["event"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_tags_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    return await storage.driver.event.aggregate_source_by_tags(source_id, time_span)


@router.get("/events/session/{session_id}", tags=["event"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_events_for_session(session_id: str, limit: int = 20):
    result = await storage.driver.event.get_events_by_session(session_id, limit)
    print(result)
    more_to_load = result.total > len(result)
    result = [{
        "id": doc["id"],
        "insert": doc["metadata"]["time"].get("insert", None),
        "status": doc["metadata"].get("status", "n/a"),
        "type": doc["type"]
    } for doc in result]

    return {"result": result, "more_to_load": more_to_load}


@router.get("/events/session/{session_id}/profile/{profile_id}", tags=["event"],
            include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_events_for_session(session_id: str, profile_id: str, limit: int = 20):
    result = await storage.driver.event.get_events_by_session_and_profile(
        profile_id,
        session_id,
        limit)

    more_to_load = result.total > len(result)
    result = [{
        "id": doc["id"],
        "metadata": doc["metadata"],
        "type": doc["type"]
    } for doc in result]

    return {"result": result, "more_to_load": more_to_load}
