from typing import Optional, List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.storage.driver.elastic.session import _aggregate_session
from tracardi.service.storage.elastic.interface.session import count_sessions_online_in_db, \
    count_online_sessions_by_location_in_db, count_sessions_in_db, refresh_session_db, flush_session_db, \
    save_sessions_in_db, load_session_from_db, delete_session_from_db, load_nth_last_session_for_profile
from tracardi.service.storage.index import Resource
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", 'marketer', "maintainer"]))]
)


@router.get("/session/count/online", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions_online():
    result = await count_sessions_online_in_db()
    return {
        "events": result.total,
        "sessions": result.aggregations("sessions").get('value', 0)
    }


@router.get("/sessions/count/by_app", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_app():
    bucket_name = 'sessions_by_app'
    result = await _aggregate_session(bucket_name, by='app.name', buckets_size=20)

    if bucket_name not in result.aggregations:
        return []

    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


@router.get("/sessions/count/by_os_name", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_os_name():
    bucket_name = 'sessions_by_os_name'
    result = await _aggregate_session(bucket_name, by='os.name', buckets_size=20)

    if bucket_name not in result.aggregations:
        return []

    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


@router.get("/sessions/count/by_device_geo", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_device_location():
    bucket_name = 'sessions_by_device_geo'
    result = await _aggregate_session(bucket_name, by='device.geo.country.name', buckets_size=20)

    if bucket_name not in result.aggregations:
        return []

    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


@router.get("/sessions/count/by_channel", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_channel():
    bucket_name = 'sessions_by_channel'
    result = await _aggregate_session(bucket_name, by='metadata.channel', buckets_size=20)

    if bucket_name not in result.aggregations:
        return []

    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


@router.get("/sessions/count/by_resolution", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_resolution():
    bucket_name = 'sessions_by_resolution'
    result = await _aggregate_session(bucket_name, by='device.resolution', buckets_size=20)

    if bucket_name not in result.aggregations:
        return []

    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


@router.get("/session/count/online/by_location", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions_by_location():
    result = await count_online_sessions_by_location_in_db()
    return {
        "events": result.total,
        "tz": [{"name": item['key'], "count": item['doc_count']} for item in result.aggregations("tz").buckets()]
    }


@router.get("/session/count", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions():
    return await count_sessions_in_db()


@router.get("/sessions/refresh", tags=["session"], include_in_schema=tracardi.expose_gui_api)
async def session_refresh():
    """
    Refreshes session index
    """
    return await refresh_session_db()


@router.get("/sessions/flash", tags=["session"], include_in_schema=tracardi.expose_gui_api)
async def session_refresh():
    """
    Flushes session index
    """
    return await flush_session_db()


@router.post("/sessions/import", tags=["session"],
             dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
             include_in_schema=tracardi.expose_gui_api)
async def import_profiles(sessions: List[Session]):
    """
    Adds given sessions to database
    """
    return await save_sessions_in_db(sessions)


@router.get("/session/{id}",
            tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            response_model=Optional[Session],
            include_in_schema=tracardi.expose_gui_api)
async def get_session_by_id(id: str, response: Response):
    """
    Returns session with given ID (str)
    """
    result = await load_session_from_db(id)

    if result is None:
        response.status_code = 404

    return result


@router.delete("/session/{id}", tags=["session"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               include_in_schema=tracardi.expose_gui_api)
async def delete_session(id: str, response: Response):
    """
    Deletes session with given ID (str)
    """
    index = Resource().get_index_constant('session')
    # Delete from all indices
    result = await delete_session_from_db(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/session/profile/{profile_id}", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_nth_last_session_for_profile(profile_id: str, n: Optional[int] = 0):

    result = await load_nth_last_session_for_profile(profile_id, n)

    if result is None:
        return None

    return {
        "id": result["id"],
        "metadata": result["metadata"],
        "context": result["context"],
        "profile": result['profile'],
        "device": result['device'],
        "app": result['app'],
        "os": result['os'],
    }
