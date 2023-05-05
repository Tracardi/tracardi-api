from typing import Optional, List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.storage.driver import storage
from tracardi.service.storage.index import resources
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", 'marketer', "maintainer"]))]
)


@router.get("/session/count/online", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=server.expose_gui_api)
async def count_sessions():
    result = await storage.driver.session.count_online()
    return {
        "events": result.total,
        "sessions": result.aggregations("sessions").get('value', 0)
    }


@router.get("/sessions/count/by_app", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=server.expose_gui_api)
async def get_sessions_by_app():
    result = await storage.driver.session.count_session_by_browser()
    return {
        "sessions": result.total,
        "browsers": [{"name": item['key'], "value": item['doc_count']} for item in
                     result.aggregations("browsers").buckets()],
    }


@router.get("/session/count/online/by_location", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=server.expose_gui_api)
async def count_sessions_by_location():
    result = await storage.driver.session.count_online_by_location()
    return {
        "events": result.total,
        "country": [{"name": item['key'], "count": item['doc_count']} for item in
                    result.aggregations("country").buckets()],
        "tz": [{"name": item['key'], "count": item['doc_count']} for item in result.aggregations("tz").buckets()]
    }


@router.get("/session/count", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=server.expose_gui_api)
async def count_sessions():
    return await storage.driver.session.count()


@router.get("/sessions/refresh", tags=["session"], include_in_schema=server.expose_gui_api)
async def session_refresh():
    """
    Refreshes session index
    """
    return await storage.driver.session.refresh()


@router.get("/sessions/flash", tags=["session"], include_in_schema=server.expose_gui_api)
async def session_refresh():
    """
    Flushes session index
    """
    return await storage.driver.session.flush()


@router.post("/sessions/import", tags=["session"],
             dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
             include_in_schema=server.expose_gui_api)
async def import_profiles(sessions: List[Session]):
    """
    Adds given sessions to database
    """
    return await storage.driver.session.save_sessions(sessions)


@router.get("/session/{id}",
            tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            response_model=Optional[Session],
            include_in_schema=server.expose_gui_api)
async def get_session_by_id(id: str, response: Response):
    """
    Returns session with given ID (str)
    """
    result = await storage.driver.session.load_by_id(id)

    if result is None:
        response.status_code = 404

    return result


@router.delete("/session/{id}", tags=["session"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               include_in_schema=server.expose_gui_api)
async def delete_session(id: str, response: Response):
    """
    Deletes session with given ID (str)
    """
    index = resources.get_index_constant('session')
    # Delete from all indices
    result = await storage.driver.session.delete_by_id(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/session/profile/{profile_id}", tags=["session"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=server.expose_gui_api)
async def get_nth_last_session_for_profile(profile_id: str, n: Optional[int] = 0):
    result = await storage.driver.session.get_nth_last_session(profile_id, n + 1)

    if result is None:
        return None

    return {
        "id": result["id"],
        "metadata": result["metadata"],
        "context": result["context"],
        "profile": result['profile']
    }
