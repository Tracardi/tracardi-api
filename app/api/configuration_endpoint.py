from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.service.grouping import get_grouped_result
from tracardi.domain.test import Test
from tracardi.service.storage.mysql.mapping.test_mapping import map_to_test
from tracardi.service.storage.mysql.service.test_service import TestService

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer", "developer"]))]
)

ts = TestService()

@router.get("/configuration/{id}", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def get_test(id: str):
    record = await ts.load_by_id(id)
    if not record.exists():
        raise HTTPException(status_code=404, detail=f"Configuration with ID {id} not found.")

    return record.map_to_object(map_to_test)


@router.get("/configuration", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def list_tests(query: Optional[str] = None, limit: int = 200):
    records = await ts.load_all(search=query, limit=limit)

    return get_grouped_result("Configuration Settings", records, map_to_test)


@router.post("/configuration", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def add_test(test: Test):
    return await ts.upsert(test)


@router.delete("/configuration/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def delete_test(id: str):
    """
    Deletes test from the database
    """
    return await ts.delete_by_id(id)
