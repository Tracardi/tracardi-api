from fastapi import APIRouter, Depends

from tracardi.domain.entity_index_mapping import EntityIndexMapping
from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer"]))]
)


@router.post("/entity/{index}", tags=["entity"], include_in_schema=server.expose_gui_api)
async def create_entity_index(index: str, mapping: EntityIndexMapping):
    index = f"entity-{index}"
    return await storage.driver.raw.create_index(index, mapping.dict(by_alias=True))


@router.get("/entity/{index}/mapping", tags=["entity"], include_in_schema=server.expose_gui_api)
async def get_entity_index_mapping(index: str):
    index = f"entity-{index}"
    return await storage.driver.raw.get_mapping(index)
