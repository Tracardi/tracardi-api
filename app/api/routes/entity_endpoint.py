from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from tracardi.service.adapter.bigdata.adapter_selector import bd_elastic_adapter

from tracardi.domain.entity_index_mapping import EntityIndexMapping
from tracardi.service.storage.elastic.interface import raw as raw_db
from tracardi.service.storage.elastic.interface import entity as entity_db
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer", "marketer"]))]
)


@router.post("/entity/{index}", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def create_entity_index(index: str, mapping: EntityIndexMapping):
    index = f"entity-{index}"
    return await raw_db.create_index(index, mapping.model_dump(by_alias=True))


@router.get("/entity/{index}/mapping", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def get_entity_index_mapping(index: str):
    try:
        index = f"entity-{index}"
        return await raw_db.get_mapping(index)
    except NotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.get("/entity/count", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def entity_count(query: dict = None):
    return await entity_db.count(query)
