from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.exceptions.exception import DuplicatedRecordException
from tracardi.service.storage.driver import storage
from tracardi.domain.profile import Profile
from tracardi.service.storage.drivers.elastic.profile import deduplicate_profile
from tracardi.service.storage.index import resources
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
async def get_profile_by_id(id: str, response: Response) -> Optional[dict]:
    """
    Returns profile with given ID (str)
    """
    try:
        record = await storage.driver.profile.load_by_id(id)
        if record is None:
            response.status_code = 404
            return None

        result = dict(record)
        result['_meta'] = record.get_meta_data()
        return result
    except DuplicatedRecordException as e:
        await deduplicate_profile(id)
        raise e


@router.delete("/profile/{id}", tags=["profile"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               response_model=Optional[dict],
               include_in_schema=server.expose_gui_api)
async def delete_profile(id: str, response: Response):
    """
    Deletes profile with given ID (str)
    """
    # Delete from all indices
    index = resources.get_index_constant("profile")
    result = await storage.driver.profile.delete_by_id(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result
