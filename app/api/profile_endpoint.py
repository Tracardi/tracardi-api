from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.service.storage.driver import storage
from tracardi.domain.profile import Profile
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/profile/count", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=server.expose_gui_api)
async def count_profiles():
    return await storage.driver.profile.count()


@router.post("/profiles/import", dependencies=[Depends(Permissions(roles=["admin"]))], tags=["profile"],
             include_in_schema=server.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    """
    Saves given profiles (list of profiles) to database. Accessible by roles: "admin"
    """
    return await storage.driver.profile.save_all(profiles)


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=server.expose_gui_api)
async def refresh_profile():
    """
    Refreshes profile index
    """
    return await storage.driver.profile.refresh()


@router.get("/profiles/flash", tags=["profile"], include_in_schema=server.expose_gui_api)
async def refresh_profile():
    """
    Flashes profile index
    """
    return await storage.driver.profile.flush()


@router.get("/profile/{id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=server.expose_gui_api)
async def get_profile_by_id(id: str, response: Response) -> Optional[Profile]:
    """
    Returns profile with given ID (str)
    """
    record = await storage.driver.profile.load_by_id(id)

    if record is None:
        response.status_code = 404
        return None

    return record.to_entity(Profile)


@router.delete("/profile/{id}", tags=["profile"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               response_model=Optional[dict],
               include_in_schema=server.expose_gui_api)
async def delete_profile(id: str, response: Response):
    """
    Deletes profile with given ID (str)
    """
    result = await storage.driver.profile.delete(id)

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/profile/logs/{id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            response_model=list, include_in_schema=server.expose_gui_api)
async def get_profile_logs(id: str):
    """
    Gets logs for profile with given ID (str)
    """
    log_records = await storage.driver.console_log.load_by_profile(id)
    return list(log_records)
