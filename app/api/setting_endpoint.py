from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.domain.setting import Setting
from tracardi.service.storage.mysql.map_to_named_entity import map_to_named_entity
from tracardi.service.storage.mysql.mapping.setting_mapping import map_to_setting
from tracardi.service.storage.mysql.service.setting_service import SettingService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import get_result_dict, get_grouped_result
from typing import Optional

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)

ss = SettingService()


@router.get("/settings/{type}/entities", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def load_setting_entities(type: str):
    """
    Returns list of setting as named entities.
    """
    raise NotImplemented("Do not use. Use audiences instead.")
    # records = await ss.load_all()
    #
    # return get_result_dict(records, map_to_named_entity)


@router.get("/setting/{type}/{id}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def get_setting(type: str, id: str):
    """
    Returns setting with given ID.
    """
    raise NotImplemented("Do not use. Use audiences instead.")
    # result = await ss.load_by_id(id)
    #
    # if not result.exists():
    #     raise HTTPException(status_code=404, detail=f"Setting with ID {id} not found.")
    #
    # return result.map_to_object(map_to_setting)


@router.get("/settings/{type}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def load_grouped_settings(type: str, query: Optional[str] = None):
    """
    Returns list of settings according to given query, grouped by tag.
    """
    raise NotImplemented("Do not use. Use audiences instead.")
    # records = await ss.load_all(search=query, limit=100)
    # return get_grouped_result("Metrics", records, map_to_setting)


@router.post("/setting/{type}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def add_setting(setting: Setting):
    """
    Adds or edits setting in the database.
    """
    raise NotImplemented("Do not use. Use audiences instead.")
    # return await ss.insert(setting)


@router.delete("/setting/{type}/{id}", tags=["setting"], include_in_schema=tracardi.expose_gui_api)
async def delete_setting(id: str):
    """
    Deletes setting from the database
    """
    raise NotImplemented("Do not use. Use audiences instead.")
    # return await ss.delete_by_id(id)
