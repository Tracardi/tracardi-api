from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Response
from tracardi.domain.enum.time_span import TimeSpan
from tracardi.service import events
from tracardi.service.events import get_default_event_type_schema
from tracardi.service.storage.driver.elastic import event as event_db
from tracardi.service.storage.driver.elastic import debug_info as debug_info_db
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi.service.wf.domain.debug_info import DebugInfo
from .auth.permissions import Permissions

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


@router.get("/events/by-type/by-source", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def get_event_types():
    """
    Returns event types along with the event sources ids.
    """

    def _get_data(result):
        for by_type in result.aggregations('by_type').buckets():
            row = {'type': by_type['key'], 'source': []}
            for bucket in by_type['by_source']['buckets']:
                row['source'].append({
                    "id": bucket['key'],
                    "count": bucket['doc_count']
                })
            yield row

    result = await event_db.aggregate_events_by_type_and_source()
    return list(_get_data(result))


@router.get("/events/refresh", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def events_refresh_index():
    """
    Refreshes event index.
    """
    return await event_db.refresh()


@router.get("/events/flush", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def events_flush_index():
    """
    Flushes event index.
    """
    return await event_db.flush()


@router.get("/event/count", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def count_events():
    return await event_db.count()


@router.get("/event/avg/requests", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def average_events():
    result = await event_db.count(query={
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


@router.get("/event/avg/process-time", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def count_avg_process_time() -> dict:
    return await event_db.get_avg_process_time()


# todo not used - not in tests
# @router.get("/events/heatmap/profile/{id}", tags=["event"], include_in_schema=tracardi.expose_gui_api)
# async def heatmap_by_profile(id: str):
#     """
#     Returns events heatmap for profile with given ID
#     """
#     bucket_name = "items_over_time"
#
#     result = await event_db.heatmap_by_profile(id, bucket_name)
#     return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]


# todo not used -  not in tests
# @router.get("/events/heatmap", tags=["event"], include_in_schema=tracardi.expose_gui_api)
# async def heatmap():
#     """
#     Returns events heatmap
#     """
#     bucket_name = "items_over_time"
#
#     result = await event_db.heatmap_by_profile(None, bucket_name)
#     return {key: value for key, value in result.process(__format_time_buckets, bucket_name)}[bucket_name]


@router.get("/events/metadata/type", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def event_types(query: str = None, limit: int = 1000):
    """
    Returns event types
    """
    return await events.get_event_types(query, limit)


@router.get("/events/by_type", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_types():
    """
    Returns number of events grouped by type
    """
    return await event_db.aggregate_event_type()


@router.get("/events/by_tag", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_tags():
    """
    Returns number of events grouped by tags
    """
    return await event_db.aggregate_event_tag()


@router.get("/events/by_status", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_statuses():
    """
    Returns number of events grouped by tags
    """
    return await event_db.aggregate_event_status()


@router.get("/events/by_device_geo", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_device_geo_location():
    """
    Returns number of events grouped by device location
    """
    return await event_db.aggregate_event_device_geo()


@router.get("/events/by_os_name", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_device_by_os():
    """
    Returns number of events grouped by operation system name
    """
    return await event_db.aggregate_event_os_name()


@router.get("/events/by_channel", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_channels():
    """
    Returns number of events grouped by channels
    """
    return await event_db.aggregate_event_channels()


@router.get("/events/by_resolution", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_resolution():
    """
    Returns number of events grouped by screen resolution
    """
    return await event_db.aggregate_event_resolution()


@router.get("/events/by_source", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def aggregate_event_by_source(buckets_size: int = 30):
    """
    Returns number of events grouped by event source
    """
    return await event_db.aggregate_events_by_source(buckets_size=buckets_size)


# todo not used -  not in tests
@router.get("/events/heatmap_by_profile/profile/{profile_id}", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def event_types_by_profile_id(profile_id: str):
    """
    Returns events heatmap for profile with given ID
    """
    return await event_db.load_events_heatmap(profile_id)


# todo not used -  not in tests
@router.get("/events/heatmap", tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def event_types_heatmap():
    """
    Returns number of events grouped by event time
    """
    return await event_db.load_events_heatmap()


@router.get("/event/{id}",
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            tags=["event"], include_in_schema=tracardi.expose_gui_api)
async def get_event(id: str, response: Response):
    """
    Returns event with given ID
    """
    record = await event_db.load(id)

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
    return await event_db.delete_by_id(id)


@router.get("/event/debug/{id}", tags=["event"], response_model=List[DebugInfo],
            include_in_schema=tracardi.expose_gui_api)
async def get_event_debug_info(id: str):
    """
    Returns debug info of event with given ID
    """
    encoded_debug_records = await debug_info_db.load_by_event(id)
    if encoded_debug_records is not None:
        debug_info = [EventDebugRecord.decode(record, from_dict=True)
                      for record in encoded_debug_records]  # type: List[DebugInfo]
        return debug_info
    return None


# todo not used -  not in tests
@router.get("/event/group/by_tags/profile/{profile_id}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api, response_model=dict)
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
    result = await event_db.aggregate_profile_events(
        profile_id=profile_id,
        aggregate_query=aggregate_query
    )
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


# todo not used -  not in tests
@router.get("/event/group/by_tags/from/{time_from}/to/{time_to}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
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
    result = await event_db.aggregate_timespan_events(
        time_from=time_from,
        time_to=time_to,
        aggregate_query=aggregate_query
    )
    del result.aggregations["for_tags"][0]["other"]
    result.aggregations["for_tags"][0]["no_tag"] = result.aggregations["for_missing_tags"][0]["found"]
    agg_results = {**result.aggregations["for_tags"][0]}
    return agg_results


@router.get("/event/for-source/{source_id}/by-type/{time_span}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_type_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    return await event_db.aggregate_source_by_type(source_id, time_span)


@router.get("/event/for-source/{source_id}/by-tag/{time_span}", tags=["event"], include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def get_for_source_grouped_by_tags_time(source_id: str, time_span: TimeSpan):
    """
    time_span: d - last day, w - last week, M - last month, y - last year
    """
    return await event_db.aggregate_source_by_tags(source_id, time_span)


@router.get("/events/session/{session_id}/profile/{profile_id}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_events_for_session(session_id: str, profile_id: str, limit: int = 20):
    result = await event_db.get_events_by_session_and_profile(
        profile_id,
        session_id,
        limit)

    more_to_load = result.total > len(result)
    result = [{
        "id": doc["id"],
        "metadata": doc["metadata"],
        "type": doc["type"],
        "name": doc.get('name', None),
        "source": doc.get('source')
    } for doc in result]

    return {"result": result, "more_to_load": more_to_load}


@router.get("/events/profile/{profile_id}", tags=["event"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_events_for_profile(profile_id: str, limit: int = 24):
    """ Load events for profile id """

    result = await event_db.get_events_by_profile(
        profile_id,
        limit)
    return result.dict()


@router.get("/event/type/{event_type}/schema", tags=["event"],
            include_in_schema=tracardi.expose_gui_api)
async def get_event_type_data_schema(event_type: str):
    """Gets pre-defined event type data schema"""

    return get_default_event_type_schema(event_type)
