from typing import Optional
from fastapi import APIRouter, HTTPException

from tracardi.service.installation import install_system, check_installation
from tracardi.config import tracardi
from tracardi.domain.credentials import Credentials
from tracardi.service.plugin.plugin_install import install_default_plugins

router = APIRouter()


@router.get("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """
    return await check_installation()


@router.get("/install/plugins", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def install_plugins():
    return await install_default_plugins()


@router.post("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install(credentials: Optional[Credentials]):

    try:
        return await install_system(credentials)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

