from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException

from tracardi.domain.entity_index_mapping import EntityIndexMapping
from tracardi.service.storage.elastic.interface.gui import storage as storage_dao
from tracardi.service.storage.elastic.interface.gui import entity as entity_dao
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer", "marketer"]))]
)


@router.post("/entity/{index}", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def create_entity_index(index: str, mapping: EntityIndexMapping):
    index = f"entity-{index}"
    mapping_dict = mapping.model_dump(by_alias=True)
    return await storage_dao.create_index(index, mapping_dict)


@router.get("/entity/{index}/mapping", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def get_entity_index_mapping(index: str):
    try:
        index = f"entity-{index}"
        return await storage_dao.load_mapping(index)
    except NotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.get("/entity/count", tags=["entity"], include_in_schema=tracardi.expose_gui_api)
async def entity_count(query: dict = None):
    return await entity_dao.count_entities(query)
