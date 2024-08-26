from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.domain.profile import Profile


from tracardi.service.storage.index import Resource

from .auth.permissions import Permissions
from tracardi.config import tracardi

from tracardi.service.storage.interface import profile_mutation_collector_dao, profile_load_collector_dao, \
    profile_gui_dao
from tracardi.service.storage.elastic.interface.gui import profile as profile_gui_dao
from tracardi.service.storage.elastic.interface.collector.mutation import profile as profile_collector_dao

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/profile/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profiles():
    """
    Returns:
        {
          "count": 77
        }
    """
    return await profile_gui_dao.profile_count()


@router.get("/profile/duplicates/count", tags=["profile"],
            include_in_schema=tracardi.expose_gui_api)
async def count_profile_duplicates(id: str):
    profile = await profile_load_collector_dao.load_profile(id.strip())
    if profile:
        return await profile_gui_dao.count_profile_duplicates(profile.ids)
    return 0


@router.post("/profiles/import", dependencies=[Depends(Permissions(roles=["admin"]))], tags=["profile"],
             include_in_schema=tracardi.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    """
    Saves given profiles (list of profiles) to database. Accessible by roles: "admin"
    """
    return await profile_collector_dao.save_profiles_in_db(profiles)


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def refresh_profile():
    """
    Refreshes profile index
    """
    return await profile_gui_dao.profile_refresh()


@router.get("/profiles/flash", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def flash_profile():
    """
    Flashes profile index
    """
    return await profile_gui_dao.profile_flush()


@router.get("/profile/{profile_id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_profile_by_id(profile_id: str, response: Response) -> Optional[dict]:
    """
    Returns profile with given ID (str)
    """

    # This is acceptable - we see the profile from the database, no cache
    record = await profile_load_collector_dao.load_profile_by_id(profile_id)

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
async def delete_profile_by_id(id: str):
    """
    Deletes profile with given ID (str)
    """
    # Delete from all indices
    index = Resource().get_index_constant("profile")
    await profile_mutation_collector_dao.delete_profile(id, index=index.get_multi_storage_alias())


@router.get("/profile/{profile_id}/by/{field}", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
async def profile_data_by(profile_id: str, field: str, table: bool = False):
    return await profile_gui_dao.load_events_by_profile_and_field(profile_id, field, table)


# @router.get("/profiles/{qualify}/segment/{segment_names}", tags=["profile"], include_in_schema=tracardi.expose_gui_api)
# async def find_profiles_by_segments(segment_names: str, qualify: str):
#     """
#     Returns profiles in given segments.
#
#     Segment names is a string with segment names, like: segment1,segment2
#     Qualify takes any string like: any or all
#     """
#
#     if qualify.lower() == 'any':
#         condition = 'should'
#     else:
#         condition = 'must'
#     records = await profile_db.load_profiles_by_segments(segment_names.split(','), condition=condition)
#     return records.dict()


@router.get('/profiles/top/modified', tags=['profile'], include_in_schema=tracardi.expose_gui_api)
async def load_top_profiles(limit: Optional[int] = 5):
    return await profile_gui_dao.load_modified_top_profiles(limit)
