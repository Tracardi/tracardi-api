from typing import List, Optional

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi.domain.profile import Profile
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "data_admin"]))]
)


@router.get("/profile/count", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "data_admin"]))],
            include_in_schema=server.expose_gui_api)
async def count_profiles():
    return await storage.driver.profile.count()


@router.post("/profiles/import", dependencies=[Depends(Permissions(roles=["admin"]))], tags=["profile"],
             include_in_schema=server.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    """
    Saves given profiles (list of profiles) to database. Accessible by roles: "admin"
    """
    try:
        return await storage.driver.profile.save_profiles(profiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=server.expose_gui_api)
async def refresh_profile():
    """
    Refreshes profile index
    """
    try:
        return await storage.driver.profile.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            response_model=Profile, include_in_schema=server.expose_gui_api)
async def get_profile_by_id(id: str, response: Response):
    """
    Returns profile with given ID (str)
    """
    try:
        profile = Profile(id=id)
        result = await StorageFor(profile).index().load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404

    return result


@router.delete("/profile/{id}", tags=["profile"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               response_model=Optional[dict],
               include_in_schema=server.expose_gui_api)
async def delete_profile(id: str, response: Response):
    """
    Deletes profile with given ID (str)
    """
    # try:
    result = await storage.driver.profile.delete(id)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

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
