import logging
from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Response
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.domain.event_source import EventSource
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.event_source_manager import event_source_types, save_source
from tracardi.service.storage.driver.elastic import event_source as event_source_db
from app.service.grouper import search
from .auth.permissions import Permissions
from tracardi.config import tracardi

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/event-sources/by_type",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def list_event_sources(query: str = None):
    """
    Lists all event sources that match given query (str) parameter
    """
    result = await event_source_db.load_all(limit=1000)

    total = result.total
    result = [EventSource(**r) for r in result]

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if query in r.name.lower() or search(query, r.type)]

    # Grouping
    groups = defaultdict(list)
    for event_source in result:  # type: EventSource
        if isinstance(event_source.groups, list):
            if len(event_source.groups) == 0:
                groups["general"].append(event_source)
            else:
                for group in event_source.groups:
                    groups[group].append(event_source)
        elif isinstance(event_source.groups, str):
            groups[event_source.groups].append(event_source)

    # Sort
    groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

    return {
        "total": total,
        "grouped": groups
    }


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

    types = event_source_types()

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
    result = await event_source_db.load(id)

    if result is None:
        response.status_code = 404
        return None

    return result


@router.post("/event-source", tags=["event-source"],
             include_in_schema=tracardi.expose_gui_api)
async def save_event_source(event_source: EventSource):
    """
    Adds new event source in database
    """
    try:
        return await save_source(event_source)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=repr(e))


@router.delete("/event-source/{id}", tags=["event-source"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_event_source(id: str, response: Response):
    """
    Deletes event source with given ID (str)
    """
    result = await event_source_db.delete_by_id(id)

    if result is None:
        response.status_code = 404
        return None

    await event_source_db.refresh()
    return True


@router.get("/event-sources/refresh",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def refresh_event_sources():
    """
    Refreshes event source index in database
    """
    return await event_source_db.refresh()


@router.get("/event-sources/entity",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def list_event_sources_names_and_ids(add_current: bool = False, type: Optional[str] = None, limit: int = 500):
    """
    Returns list of event sources. This list contains only id and name.
    """

    if type:
        result = await event_source_db.load_by(field="type", value=type)
    else:
        result = await event_source_db.load_all(limit=limit)

    if result is None:
        return {
            "total": 0,
            "result": []
        }
    total = result.total
    result = [NamedEntity(id=r['id'], name=f"{r['name']} ({','.join(r['type']) if isinstance(r['type'], list) else r['type']})") for r in result]

    if add_current is True:
        total += 1
        result.append(NamedEntity(id="@current-source", name="@current-source"))

    return {
        "total": total,
        "result": result
    }
