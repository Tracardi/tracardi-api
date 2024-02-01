import logging
from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, Depends, Response

from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.mysql.mapping.event_source_mapping import map_to_event_source
from tracardi.service.storage.mysql.service.event_source_service import EventSourceService
from tracardi.exceptions.log_handler import get_logger
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import get_grouped_result

logger = get_logger(__name__)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

@router.get("/event-sources",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
# Obsolete
@router.get("/event-sources/by_type",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def list_event_sources(query: str = None):
    """
    Lists all event sources that match given query (str) parameter
    """

    records = await EventSourceService().load_all_in_deployment_mode(query, limit=500)

    return get_grouped_result("Event sources", records, map_to_event_source)


@router.get("/event-sources/type/{type}",
            tags=["event-source"],
            response_model=dict,
            include_in_schema=tracardi.expose_gui_api)
async def get_event_source_types(type: TypeEnum) -> dict:
    """
    Returns a list of event source types. Each event source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    types = EventSourceService.event_source_types()

    if type.value == 'name':
        types = {id: t['name'] for id, t in types.items()}

    return {
        "total": len(types),
        "result": types
    }


@router.get("/event-source/{id}", tags=["event-source"],
            response_model=Optional[EventSource],
            include_in_schema=tracardi.expose_gui_api)
async def load_event_source(id: str, response: Response):
    """
    Returns event source with given ID (str)
    """

    record = await EventSourceService().load_by_id_in_deployment_mode(id)

    if not record.exists():
        response.status_code = 404
        return None

    return record.map_to_object(map_to_event_source)


@router.post("/event-source", tags=["event-source"],
             include_in_schema=tracardi.expose_gui_api)
async def save_event_source(event_source: EventSource):
    """
    Adds new event source in database
    """
    return await EventSourceService().save(event_source)

@router.delete("/event-source/{source_id}", tags=["event-source"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_event_source(source_id: str):
    """
    Deletes event source with given ID (str).
    Return False if it is available in draft or production. True if all the instances where deleted
    """

    return await EventSourceService().delete_by_id_in_deployment_mode(source_id)

@router.get("/event-sources/entity",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def list_event_sources_names_and_ids(add_current: bool = False, type: Optional[str] = None):
    """
    Returns list of event sources. This list contains only id and name.
    """
    ess = EventSourceService()
    if type:
        records = await ess.load_by_type_in_deployment_mode(type)
    else:
        records = await ess.load_all_in_deployment_mode()

    if not records.exists():
        return {
            "total": 0,
            "result": []
        }

    total = records.count()
    result = records.as_named_entities(rewriter=lambda r: f"{r.name} ({r.type})")

    if add_current is True:
        total += 1
        result.append(NamedEntity(id="@current-source", name="@current-source"))

    return {
        "total": total,
        "result": result
    }
