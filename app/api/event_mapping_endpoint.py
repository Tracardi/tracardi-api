from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.event_type_metadata import EventTypeMetadata
from tracardi.service.events import get_default_mappings_for
from typing import Optional, List

from tracardi.service.license import License
from tracardi.service.storage.mysql.interface import event_mapping_dao

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event-type"
)


@router.post("/mapping", tags=["event-type"], include_in_schema=tracardi.expose_gui_api)
async def add_event_type_mapping(event_mapping: EventTypeMetadata):
    """
    Creates new event type mapping in database
    """
    return await event_mapping_dao.insert(event_mapping)


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

    records, total = await event_mapping_dao.load_by_event_type(event_type)

    if records:
        mappings.extend(records)
    else:
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type}] not found.")

    return {
        "total": len(mappings),
        "result": mappings
    }


@router.get("/mapping/{event_type_id}",
            tags=["event-type"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=Optional[EventTypeMetadata])
async def get_event_mapping_by_id(event_type_id: str):
    """
    Return custom event type mapping for given event type
    """
    record = await event_mapping_dao.load_by_id(event_type_id)

    if not record:
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type_id}] not found.")

    return record


@router.delete("/mapping/{event_type_id}", tags=["event-type"], include_in_schema=tracardi.expose_gui_api)
async def del_event_type_metadata(event_type_id: str):
    """
    Deletes event type metadata for given event type
    """

    return await event_mapping_dao.delete_by_id(event_type_id)


@router.get("/search/mappings", tags=["event-type"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def list_event_type_mappings_by_tag(query: str = None, start: Optional[int] = None, limit: Optional[int] = 200):
    """
    Lists event type metadata by tag, according to given start (int), limit (int) and query (str)
    """

    if not License.has_license():
        raise HTTPException(status_code=402, detail="Missing license.")

    records, total = await event_mapping_dao.load_all(search=query, limit=limit, offset=start)

    return {
        "total": max([total, len(records)]),
        "grouped": {
            "Event mappings": records
        }
    }
