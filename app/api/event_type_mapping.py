import asyncio
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.grouping import group_records
from tracardi.domain.event_type_metadata import EventTypeMetadata
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from tracardi.service.events import get_default_mappings_for
from tracardi.service.storage.driver.elastic import event_management as event_management_db
from tracardi.service.storage.driver.elastic import event as event_db
from typing import Optional

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event-type"
)


@router.put("/mapping/refresh", tags=["event-type"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_event_type_mapping():
    """
    Refreshes event type mapping
    """
    return await event_management_db.refresh()


@router.post("/mapping", tags=["event-type"], include_in_schema=server.expose_gui_api,
             response_model=BulkInsertResult)
async def add_event_type_mapping(event_mapping: EventTypeMetadata):
    """
    Creates new event type mapping in database
    """

    # Save tags
    result = await event_management_db.save(event_mapping)
    await event_management_db.refresh()

    if result.errors:
        raise ValueError(result.errors)

    # Update events for new tags in background

    task = event_db.update_tags(
        event_type=event_mapping.event_type,
        tags=event_mapping.tags)

    asyncio.create_task(task)

    return result


@router.get("/mappings/{event_type}",
            tags=["event-type"],
            include_in_schema=server.expose_gui_api,
            response_model=dict)
async def list_event_type_metadata(event_type: str):
    """
    Returns a list of event type mappings both build-in and custom for given event type
    """

    records = []

    build_in = get_default_mappings_for(event_type, "copy")
    if build_in is not None:
        build_in = {
            'id': str(uuid4()),
            'name': 'Build in mapping',
            'event_type': event_type, 'description': f"\"{event_type}\" event mapping.",
            'enabled': True,
            'index_schema': build_in,
            'tags': ['General'],
            'build_in': True
        }
        records.append(build_in)

    record = await event_management_db.get_event_type_mapping(event_type)
    if record is not None:
        record['build-in'] = False
        records.append(record)

    if not records:
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type}] not found.")

    return {
        "total": len(records),
        "result": records
    }


@router.get("/mapping/{event_type}",
            tags=["event-type"],
            include_in_schema=server.expose_gui_api,
            response_model=Optional[dict])
async def get_event_type_mapping(event_type: str):
    """
    Return custom event type mapping for given event type
    """

    record = await event_management_db.get_event_type_mapping(event_type)

    if not record:
        raise HTTPException(status_code=404, detail=f"Mapping for event type [{event_type}] not found.")

    return record


@router.delete("/mapping/{event_type}", tags=["event-type"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def del_event_type_metadata(event_type: str):
    """
    Deletes event type metadata for given event type
    """
    result = await event_management_db.del_event_type_mapping(event_type)
    await event_management_db.refresh()

    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/search/mappings", tags=["event-type"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def list_event_type_mappings_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 200):
    """
    Lists event type metadata by tag, according to given start (int), limit (int) and query (str)
    """
    result = await event_management_db.load_events_type_mapping(start, limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
