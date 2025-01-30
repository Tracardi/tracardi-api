from typing import Optional, List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.dependency.adapters.big_data_adapter import *
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", 'marketer', "maintainer"]))]
)


@router.get("/session/count/online", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions_online():
    online_events_count, online_session_count = await bd_session_adapter.count_sessions_online_in_db()
    return {
        "events": online_events_count,
        "sessions": online_session_count
    }


@router.get("/sessions/count/by_app", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_app():
    return await bd_session_adapter.agg_sessions_by_app()


@router.get("/sessions/count/by_os_name", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_os_name():
    return await bd_session_adapter.agg_sessions_by_os_name()


@router.get("/sessions/count/by_device_geo", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_device_location():
    return await bd_session_adapter.agg_sessions_by_device_location()


@router.get("/sessions/count/by_channel", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_channel():
    return await bd_session_adapter.agg_sessions_by_channel()


@router.get("/sessions/count/by_resolution", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_sessions_by_resolution():
    return await bd_session_adapter.agg_sessions_by_resolution()


@router.get("/session/count/online/by_location", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions_by_location():
    events_count, tz_list = await bd_session_adapter.count_online_sessions_by_location_in_db()
    return {
            "events": events_count,
            "tz": tz_list
        }


@router.get("/session/count", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_sessions():
    return await bd_session_adapter.count_sessions_in_db()


@router.get("/sessions/refresh", tags=["session"], include_in_schema=tracardi.expose_gui_api)
async def session_refresh():
    """
    Refreshes session index
    """
    return await bd_session_adapter.refresh_session_db()


@router.get("/sessions/flash", tags=["session"], include_in_schema=tracardi.expose_gui_api)
async def session_refresh():
    """
    Flushes session index
    """
    return await bd_session_adapter.flush_session_db()


@router.post("/sessions/import", tags=["session"],
             dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
             include_in_schema=tracardi.expose_gui_api)
async def import_profiles(sessions: List[Session]):
    """
    Adds given sessions to database
    """
    return await bd_session_adapter.save_sessions_in_db(sessions)


@router.get("/session/{id}",
            tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            response_model=Optional[Session],
            include_in_schema=tracardi.expose_gui_api)
async def get_session_by_id(id: str, response: Response):
    """
    Returns session with given ID (str)
    """
    result = await bd_session_adapter.load_session_from_db(id)

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
    index = bd_raw_adapter.get_write_index("profile")
    # Delete from all indices
    result = await bd_session_adapter.delete_session_from_db(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/session/profile/{profile_id}", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_nth_last_session_for_profile(profile_id: str, n: Optional[int] = 0):
    result = await bd_session_adapter.load_nth_last_session_for_profile(profile_id, n)

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
