from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.domain.storage_results import StorageResults
from tracardi.service.dependency.adapters.big_data_adapter import *
from tracardi.domain.profile import Profile
from tracardi.service.collector.load.flat_profile import load_flat_profile
from tracardi.service.collector.mutation import profile as mutation_profile_db

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/profile/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profiles():
    return await bd_profile_adapter.count()


@router.get("/profile/duplicates/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profile_duplicates(id: str):
    flat_profile = await load_flat_profile(id)
    if flat_profile:
        return await bd_profile_adapter.count_profile_duplicates(flat_profile.ids)
    return 0


@router.post("/profiles/import", dependencies=[Depends(Permissions(roles=["admin"]))], tags=["profile"],
             include_in_schema=tracardi.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    """
    Saves given profiles (list of profiles) to database. Accessible by roles: "admin"
    """
    return await bd_profile_adapter.save_profiles(profiles)


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def refresh_profile():
    """
    Refreshes profile index
    """
    return await bd_profile_adapter.refresh()


@router.get("/profiles/flash", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def flash_profile():
    """
    Flashes profile index
    """
    return await bd_profile_adapter.flush()


@router.get("/profile/{profile_id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_profile_by_id(profile_id: str, response: Response) -> Optional[dict]:
    """
    Returns profile with given ID (str)
    """

    # This is acceptable - we see the profile from the database
    result = await bd_profile_adapter.load_by_id_as_dict(profile_id)

    if result is None:
        response.status_code = 404
        return None

    return result


@router.delete("/profile/{id}", tags=["profile"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               response_model=Optional[dict],
               include_in_schema=tracardi.expose_gui_api)
async def delete_profile_by_id(id: str, response: Response):
    """
    Deletes profile with given ID (str)
    """
    # Delete from all indices
    index = bd_raw_adapter.get_write_index("profile")
    result = await mutation_profile_db.delete_profile(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/profile/{profile_id}/by/{field}", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def profile_data_by(profile_id: str, field: str, table: bool = False):
    return await bd_event_adapter.aggregate_profile_events_by_field(profile_id, field, table)


@router.get('/profiles/top/modified', tags=['profile'], include_in_schema=tracardi.expose_gui_api)
async def load_top_profiles(limit: Optional[int] = 5):
    result = await bd_profile_adapter.load_modified_top_profiles(limit)

    return StorageResults(
        total=len(result),
        result=result
    )
