import logging
from collections import defaultdict
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Response
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.driver import storage
from .auth.authentication import get_current_user
from app.service.grouper import search
from ..config import server
from ..service.tracardi_pro_inbound_sources import get_tracardi_pro_services

logger = logging.getLogger(__name__)

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


async def event_source_types():
    standard_inbound_sources = {
        "javascript": {
            "name": "Javascript",
            "tags": ["javascript", "inbound"]
        },
        "api-call": {
            "name": "Api call",
            "tags": ["api-call", "inbound"]
        },
    }
    try:
        endpoint = await storage.driver.pro.read_pro_service_endpoint()
        if endpoint is not None:
            for service in await get_tracardi_pro_services(endpoint):
                standard_inbound_sources[service["id"]] = {
                    "name": "{} ({})".format(service["name"], service['prefix']),
                    "tags": service["tags"] if "tags" in service else []
                }
    except Exception as e:
        logger.error(repr(e))

    return standard_inbound_sources


@router.get("/event-sources/by_type",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def list_event_sources(query: str = None):
    try:

        result, total = await storage.driver.event_source.load_all(limit=1000)

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-sources/type/{type}",
            tags=["event-source"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def get_event_source_types(type: TypeEnum) -> dict:
    """
    Returns a list of event source types. Each event source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    try:
        types = await event_source_types()

        if type.value == 'name':
            types = {id: t['name'] for id, t in types.items()}

        return {
            "total": len(types),
            "result": types
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-source/{id}", tags=["event-source"],
            response_model=Optional[EventSource],
            include_in_schema=server.expose_gui_api)
async def load_event_source(id: str, response: Response):
    try:
        result = await storage.driver.event_source.load(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404
        return None

    return result


@router.post("/event-source", tags=["event-source"],
             include_in_schema=server.expose_gui_api)
async def save_event_source(event_source: EventSource):
    try:
        types = await event_source_types()
        if event_source.type in types:
            result = await storage.driver.event_source.save(event_source)
            if result.is_nothing_saved():
                raise ValueError("Could not save event source.")
            return result
        else:
            raise ValueError("Unknown event source type {}. Available {}.".format(event_source.type, types))

    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@router.delete("/event-source/{id}", tags=["event-source"],
               include_in_schema=server.expose_gui_api)
async def delete_event_source(id: str, response: Response):
    try:
        result = await storage.driver.event_source.delete(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404
        return None

    try:
        await storage.driver.event_source.refresh()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/event-sources/refresh",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def refresh_event_sources():
    return await storage.driver.event_source.refresh()


@router.get("/event-sources/entity",
            tags=["event-source"],
            include_in_schema=server.expose_gui_api)
async def list_event_sources_names_and_ids(limit: int = 500):
    """
    Returns list of event sources. This list contains only id and name.
    """

    try:
        result, total = await storage.driver.event_source.load_all(limit=limit)
        result = [NamedEntity(**r.dict()) for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
