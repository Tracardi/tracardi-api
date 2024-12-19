from typing import List, Dict, Any, Union

from app.api.auth.permissions import Permissions
from tracardi.config import *
from fastapi import APIRouter, Depends
from tracardi.domain.settings import SystemSettings
from tracardi.service.cluster.settings import GlobalSettings
from tracardi.service.setup.setup_envs import list_system_envs, get_system_envs

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/system/settings", tags=["system"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=List[SystemSettings])
async def get_system_settings() -> List[SystemSettings]:
    """
    Lists all system settings
    """
    return await list_system_envs()


@router.get("/system/envs", tags=["system"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=Dict[str, Any])
async def get_system_envs_list() -> Dict[str, Any]:
    """
    Lists all system settings as key value
    """
    return get_system_envs()


@router.put("/cluster/settings/{key}", tags=["system"],
            include_in_schema=tracardi.expose_gui_api,
            response_model=bool)
async def set_cluster_setting(key: str, value: Union[float, bool, str]):
    if value == 'true':
        value = True
    elif value == 'false':
        value = False
    elif value.isnumeric():
        value = float(value)
    return await GlobalSettings().set(key, value)


@router.get("/cluster/settings/{key}", tags=["system"],
            include_in_schema=tracardi.expose_gui_api)
async def set_cluster_setting(key: str):
    return await GlobalSettings().get(key)