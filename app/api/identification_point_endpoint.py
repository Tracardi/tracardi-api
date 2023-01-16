from typing import Optional
from fastapi import APIRouter, Depends
from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer"]))]
)


@router.get("/identification/points", tags=["identification"], include_in_schema=server.expose_gui_api)
async def get_identification_points(query: Optional[str] = None, start: int = 0, limit: int = 100):
    result = await storage.driver.identification.load_all(start=start, limit=limit)
    return group_records(result, query, group_by=None, search_by='name', sort_by='name')


@router.get("identification/point/{id}", tags=["identification"], include_in_schema=server.expose_gui_api)
async def get_identification_point(id: str):
    return await storage.driver.identification.load_by_id(id)


@router.delete("identification/point/{id}", tags=["identification"], include_in_schema=server.expose_gui_api)
async def delete_identification_point(id: str):
    result = await storage.driver.identification.delete_by_id(id)
    await storage.driver.data_compliance.refresh()
    return result
