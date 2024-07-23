from tracardi.service.storage.mysql.interface import event_source_dao
from typing import Optional

from fastapi import APIRouter, Depends, Response

from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.domain.event_source import EventSource
from tracardi.exceptions.log_handler import get_logger
from .auth.permissions import Permissions
from tracardi.config import tracardi

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

    records, count = await event_source_dao.load_all_event_sources(query, limit=500)

    return {
        "total": count,
        "grouped": {
            "Event sources": records
        }
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
    types, count = event_source_dao.load_event_source_types(type.value)

    return {
        "total": count,
        "result": types
    }


@router.get("/event-source/{id}", tags=["event-source"],
            response_model=Optional[EventSource],
            include_in_schema=tracardi.expose_gui_api)
async def load_source_by_id(id: str, response: Response):
    """
    Returns event source with given ID (str)
    """

    record = await event_source_dao.load_event_source_by_id(id)

    if not record:
        response.status_code = 404
        return None

    return record


@router.post("/event-source", tags=["event-source"],
             include_in_schema=tracardi.expose_gui_api)
async def save_event_source(event_source: EventSource):
    """
    Adds new event source in database
    """
    return await event_source_dao.insert_event_source(event_source)


@router.delete("/event-source/{source_id}", tags=["event-source"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_event_source(source_id: str):
    """
    Deletes event source with given ID (str).
    Return False if it is available in draft or production. True if all the instances where deleted
    """

    return await event_source_dao.delete_event_source(source_id)


@router.get("/event-sources/entity",
            tags=["event-source"],
            include_in_schema=tracardi.expose_gui_api)
async def list_event_sources_names_and_ids(add_current: bool = False, type: Optional[str] = None):
    """
    Returns list of event sources. This list contains only id and name.
    """

    entities, count = await event_source_dao.load_event_source_entities(add_current, type)
    return {
        "total": count,
        "result": entities
    }

    # ess = EventSourceService()
    # if type:
    #     records = await ess.load_by_type_in_deployment_mode(type)
    # else:
    #     records = await ess.load_all_in_deployment_mode()
    #
    # if not records.exists():
    #     return {
    #         "total": 0,
    #         "result": []
    #     }
    #
    # total = records.count()
    # result = records.as_named_entities(rewriter=lambda r: f"{r.name} ({r.type})")
    #
    # if add_current is True:
    #     total += 1
    #     result.append(NamedEntity(id="@current-source", name="@current-source"))
    #
    # return {
    #     "total": total,
    #     "result": result
    # }
