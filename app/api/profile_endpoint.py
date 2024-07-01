from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.domain.profile import Profile
from tracardi.service.storage.driver.elastic import profile as profile_db
from tracardi.service.storage.driver.elastic.profile import load_modified_top_profiles
from tracardi.service.storage.elastic.interface.event import load_events_by_profile_and_field
from tracardi.service.storage.index import Resource
from tracardi.service.tracking.storage.profile_storage import delete_profile, load_profile
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/profile/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profiles():
    return await profile_db.count()


@router.get("/profile/duplicates/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profile_duplicates(id: str):
    profile = await load_profile(id)
    if profile:
        result = await profile_db.count_profile_duplicates(profile.ids)
        return result.get("count", 0)
    return 0


@router.post("/profiles/import", dependencies=[Depends(Permissions(roles=["admin"]))], tags=["profile"],
             include_in_schema=tracardi.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    """
    Saves given profiles (list of profiles) to database. Accessible by roles: "admin"
    """
    return await profile_db.save_all(profiles)


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def refresh_profile():
    """
    Refreshes profile index
    """
    return await profile_db.refresh()


@router.get("/profiles/flash", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def flash_profile():
    """
    Flashes profile index
    """
    return await profile_db.flush()


@router.get("/profile/{profile_id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_profile_by_id(profile_id: str, response: Response) -> Optional[dict]:
    """
    Returns profile with given ID (str)
    """

    # This is acceptable - we see the profile from the database
    record = await profile_db.load_by_id(profile_id)

    if record is None:
        response.status_code = 404
        return None

    result = dict(record)
    result['_meta'] = record.get_meta_data()
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
    index = Resource().get_index_constant("profile")
    result = await delete_profile(id, index=index.get_multi_storage_alias())

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/profile/{profile_id}/by/{field}", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def profile_data_by(profile_id: str, field: str, table: bool = False):
    return await load_events_by_profile_and_field(profile_id, field, table)


@router.get("/profiles/{qualify}/segment/{segment_names}", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def find_profiles_by_segments(segment_names: str, qualify: str):
    """
    Returns profiles in given segments.

    Segment names is a string with segment names, like: segment1,segment2
    Qualify takes any string like: any or all
    """

    if qualify.lower() == 'any':
        condition = 'should'
    else:
        condition = 'must'
    records = await profile_db.load_profiles_by_segments(segment_names.split(','), condition=condition)
    return records.dict()


@router.get('/profiles/top/modified', tags=['profile'], include_in_schema=tracardi.expose_gui_api)
async def load_top_profiles(limit: Optional[int] = 5):
    result = await load_modified_top_profiles(limit)
    return result.dict()
