from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.event_type_metadata import EventTypeMetadata
from tracardi.service.events import get_default_mappings_for
from typing import Optional, List

from tracardi.service.storage.mysql.mapping.event_to_event_mapping import map_to_event_mapping
from tracardi.service.storage.mysql.service.event_mapping_service import EventMappingService

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event-type"
)


@router.post("/mapping", tags=["event-type"], include_in_schema=tracardi.expose_gui_api)
async def add_event_type_mapping(event_mapping: EventTypeMetadata):
    """
    Creates new event type mapping in database
    """

    ems = EventMappingService()
    return await ems.insert(event_mapping)

    # # Save tags
    # result = await event_management_db.save(event_mapping)
    # await event_management_db.refresh()
    #
    # if result.errors:
    #     raise ValueError(result.errors)
    #
    # return result


@router.get("/mappings/{event_type}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def list_event_mappings(event_type: str):
    """
    Returns a list of event type mappings both build-in and custom for given event type
    """

    mappings: List[EventTypeMetadata] = []

    build_in = get_default_mappings_for(event_type, "copy")
    if build_in is not None:
        build_in = EventTypeMetadata(**{
            'id': str(uuid4()),
            'name': 'Build in mapping',
            'event_type': event_type, 'description': f"\"{event_type}\" event mapping.",
            'enabled': True,
            'index_schema': build_in,
            'tags': ['General'],
            'build_in': True
        })
        mappings.append(build_in)

    ems = EventMappingService()
    records = await ems.load_by_event_type(event_type)

    # record = await event_management_db.get_event_type_mapping(event_type)
    if records.exists():
        for record in records.map_to_objects(map_to_event_mapping):
            mappings.append(record)

    if not records:
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type}] not found.")

    return {
        "total": len(records),
        "result": records
    }


@router.get("/mapping/{event_type_id}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=Optional[EventTypeMetadata])
async def get_event_mapping_by_id(event_type_id: str):
    """
    Return custom event type mapping for given event type
    """

    ems = EventMappingService()
    record =  await ems.load_by_id(event_type_id)

    if not record.exists():
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type_id}] not found.")

    return record.map_to_object(map_to_event_mapping)


@router.delete("/mapping/{event_type_id}", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
               response_model=dict)
async def del_event_type_metadata(event_type_id: str):
    """
    Deletes event type metadata for given event type
    """
    ems = EventMappingService()
    return await ems.delete_by_id(event_type_id)


@router.get("/search/mappings", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def list_event_type_mappings_by_tag(query: str = None, start: Optional[int] = None, limit: Optional[int] = 200):
    """
    Lists event type metadata by tag, according to given start (int), limit (int) and query (str)
    """

    ems = EventMappingService()
    records = await ems.load_all(search=query, limit=limit, offset=start)

    return {
        "total": records.count(),
        "grouped": {
            "Event mappings": list(records.map_to_objects(map_to_event_mapping))
        }
    }