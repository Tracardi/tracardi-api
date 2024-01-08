from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from tracardi.exceptions.exception import DuplicatedRecordException
from tracardi.domain.profile import Profile
from tracardi.service.profile_deduplicator import deduplicate_profile
from tracardi.service.storage.driver.elastic import profile as profile_db
from tracardi.service.storage.driver.elastic import event as event_db
from tracardi.service.storage.index import Resource
from tracardi.service.tracking.storage.profile_storage import delete_profile
from .auth.permissions import Permissions
from tracardi.config import tracardi


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/profile/count", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def count_profiles():
    return await profile_db.count()


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


@router.get("/profile/{id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_profile_by_id(id: str, response: Response) -> Optional[dict]:
    """
    Returns profile with given ID (str)
    """
    try:
        # This is acceptable - we see the profile from the database
        record = await profile_db.load_by_id(id)
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
    bucket_name = f"by_{field}"
    result = await event_db.aggregate_profile_events_by_field(profile_id,
                                                              field=field,
                                                              bucket_name=bucket_name)

    if table:
        return {id: count for id, count in result.aggregations[bucket_name][0].items()}
    return [{"name": id, "value": count} for id, count in result.aggregations[bucket_name][0].items()]


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
