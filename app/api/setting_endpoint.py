from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.domain.setting import Setting
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import group_records
from tracardi.service.storage.driver.elastic import setting as setting_db
from typing import Optional


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/settings/{type}/entities", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def load_setting_entities(type: str):
    """
    Returns list of setting as named entities.
    """
    return {"result": [dict(id=report.id, name=report.name) for report in await setting_db.load_all(type)]}


@router.get("/setting/{type}/{id}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def get_setting(type: str, id: str):
    """
    Returns setting with given ID.
    """
    result = await setting_db.load(type, id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"Report with ID {id} not found.")

    return result


@router.get("/settings/{type}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def load_grouped_settings(type: str, query: Optional[str] = None):
    """
    Returns list of settings according to given query, grouped by tag.
    """
    result = await setting_db.load_for_grouping(type, query)
    return group_records(result, None)


@router.post("/setting/{type}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def add_setting(setting: Setting):
    """
    Adds or edits setting in the database.
    """
    if setting.type == type:
        raise TypeError("Incorrect type.")

    result = await setting_db.upsert(setting)
    await setting_db.refresh()
    return result


@router.delete("/setting/{type}/{id}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def delete_setting(id: str):
    """
    Deletes setting from the database
    """
    result = await setting_db.delete(id)
    await setting_db.refresh()
    return result
