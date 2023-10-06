from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from app.service.grouping import group_records
from tracardi.domain.event_to_profile import EventToProfile
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from tracardi.service.events import get_default_mappings_for
from tracardi.service.storage.driver.elastic import event_to_profile as event_to_profile_db
from typing import Optional

from tracardi.service.string_manager import capitalize_event_type_id

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.put("/event-to-profile/refresh", tags=["event-to-profile"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def refresh_event_to_profile():
    """
    Refreshes event to profile index
    """
    return await event_to_profile_db.refresh()


@router.post("/event-to-profile", tags=["event-to-profile"], include_in_schema=tracardi.expose_gui_api,
             response_model=BulkInsertResult)
async def add_event_to_profile(event_to_profile: EventToProfile):
    """
    Creates new event to profile record in database
    """

    result = await event_to_profile_db.save(event_to_profile)
    await event_to_profile_db.refresh()

    if result.errors:
        raise ValueError(result.errors)

    return result


@router.get("/event-to-profiles/type/{event_type}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_event_to_profile_by_event_type(event_type: str):
    """
    Returns event to profile schema for given event type
    """

    records = []
    build_in = get_default_mappings_for(event_type, "profile")
    if build_in is not None:
        build_in = {
            'id': str(uuid4()),
            'name': 'Build-in event to profile mapping',
            'event_type': {'id': event_type, 'name': capitalize_event_type_id(event_type)},
            'description': f"This is build-in system profile mapping for event type \"{event_type}\"",
            'enabled': True,
            'build_in': True,
            'config': {},
            'event_to_profile': [
                {
                    'event': {'value': item[0], 'ref': True},
                    'op': item[1],
                    'profile': {'value': source, 'ref': True}
                } for source, item in build_in.items()
            ],
            'tags': ['General']}
        records.append(build_in)

    custom_records = await event_to_profile_db.get_event_to_profile(event_type)
    if custom_records is not None:
        custom_records = custom_records.dict()
        for item in custom_records['result']:
            item['build_in'] = False
            records.append(item)

    total = len(records)

    if total == 0:
        raise HTTPException(status_code=404, detail=f"Event to profile coping schema for {event_type} not found.")

    return {
        "total": total,
        "result": records
    }


@router.get("/event-to-profile/{event_id}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_event_to_profile_by_event_id(event_id: str):
    """
    Returns event to profile schema for given event id
    """

    record = await event_to_profile_db.load_by_id(event_id)
    if record is None:
        raise HTTPException(status_code=404,
                            detail=f"Event to profile coping schema for event id {event_id} not found.")
    return record


@router.delete("/event-to-profile/{event_type}", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
               response_model=dict)
async def del_event_type_metadata(event_type: str):
    """
    Deletes event to profile schema for given event type
    """
    result = await event_to_profile_db.del_event_type_metadata(event_type)
    await event_to_profile_db.refresh()

    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/events-to-profiles", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
            response_model=list)
async def list_events_to_profiles(start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    List all of events to profiles.
    """

    result = await event_to_profile_db.load_events_to_profiles(start, limit)
    return list(result)


@router.get("/events-to-profiles/by_tag", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def list_events_to_profiles_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists events to profiles coping schema by tag, according to given start (int), limit (int) and query (str)
    """
    result = await event_to_profile_db.load_events_to_profiles(start, limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
