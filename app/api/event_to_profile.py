from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.service.grouping import get_grouped_result
from tracardi.config import tracardi
from tracardi.domain.event_to_profile import EventToProfile
from tracardi.service.events import get_default_mappings_for
from typing import Optional

from tracardi.service.storage.mysql.mapping.event_to_profile_mapping import map_to_event_to_profile
from tracardi.service.storage.mysql.service.event_to_profile_service import EventToProfileMappingService
from tracardi.service.string_manager import capitalize_event_type_id

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/event-to-profile", tags=["event-to-profile"], include_in_schema=tracardi.expose_gui_api)
async def add_event_to_profile(event_to_profile: EventToProfile):
    """
    Creates new event to profile record in database
    """

    etpms = EventToProfileMappingService()
    return await etpms.insert(event_to_profile)


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
        build_in = EventToProfile(**{
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
            'tags': ['General']})
        records.append(build_in)

    etpms = EventToProfileMappingService()
    custom_records = await etpms.load_by_type(event_type)

    if custom_records.exists():
        for event_to_profile in custom_records.map_to_objects(map_to_event_to_profile):
            event_to_profile.build_in = False
            records.append(event_to_profile)

    total = len(records)

    if total == 0:
        raise HTTPException(status_code=404, detail=f"Event to profile coping schema for {event_type} not found.")

    return {
        "total": total,
        "result": records
    }


@router.get("/event-to-profile/{id}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=Optional[EventToProfile])
async def get_event_to_profile_by_event_type_id(id: str):
    """
    Returns event to profile schema for given event id
    """

    etpms = EventToProfileMappingService()
    record = await etpms.load_by_id(id)

    if not record.exists():
        raise HTTPException(status_code=404,
                            detail=f"Event to profile coping schema for id {id} not found.")

    return record.map_to_object(map_to_event_to_profile)


@router.delete("/event-to-profile/{id}", tags=["event-type"], include_in_schema=tracardi.expose_gui_api)
async def del_event_type_metadata(id: str):
    """
    Deletes event to profile schema for given event type
    """

    etpms = EventToProfileMappingService()
    return await etpms.delete_by_id(id)


@router.get("/events-to-profiles/by_tag", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def list_events_to_profiles_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists events to profiles coping schema by tag, according to given start (int), limit (int) and query (str)
    """

    etpms = EventToProfileMappingService()
    records = await etpms.load_all(search=query, limit=limit, offset=start)

    return get_grouped_result("Mappings", records, map_to_event_to_profile)

