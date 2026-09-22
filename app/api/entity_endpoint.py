from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException

from tracardi.domain.entity_index_mapping import EntityIndexMapping
from tracardi.service.storage.elastic.interface import raw as raw_db
from tracardi.service.storage.elastic.interface import entity as entity_db
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer", "marketer"]))]
)


@router.post("/entity/{index}", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def create_entity_index(index: str, mapping: EntityIndexMapping):
    if not tracardi.enable_entities:
        raise HTTPException(status_code=404, detail="Entities are disabled via ENABLE_ENTITIES setting.")
    index = f"entity-{index}"
    return await raw_db.create_index(index, mapping.model_dump(by_alias=True))


@router.get("/entity/{index}/mapping", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def get_entity_index_mapping(index: str):
    if not tracardi.enable_entities:
        raise HTTPException(status_code=404, detail="Entities are disabled via ENABLE_ENTITIES setting.")
    try:
        index = f"entity-{index}"
        return await raw_db.get_mapping(index)
    except NotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.get("/entity/count", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def entity_count(query: dict = None):
    if not tracardi.enable_entities:
        raise HTTPException(status_code=404, detail="Entities are disabled via ENABLE_ENTITIES setting.")
    return await entity_db.count(query)
