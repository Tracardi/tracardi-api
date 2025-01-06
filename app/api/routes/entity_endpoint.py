from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException

from tracardi.domain.entity_index_mapping import EntityIndexMapping
from tracardi.service.adapter.bigdata.adapter_selector import bd_entity_adapter
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer", "marketer"]))]
)

_bd_entity_adapter = bd_entity_adapter()


@router.post("/entity/{index}", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def create_entity_index(index: str, mapping: EntityIndexMapping):
    return await _bd_entity_adapter.create_entity(index, mapping.model_dump(by_alias=True))


@router.get("/entity/{index}/mapping", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def get_entity_index_mapping(index: str):
    try:
        return await _bd_entity_adapter.get_entity_mapping(index)
    except NotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.get("/entity/count", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def entity_count(query: dict = None):
    return await _bd_entity_adapter.count(query)
