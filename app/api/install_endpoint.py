from typing import Optional
from fastapi import APIRouter, HTTPException

from tracardi.domain.installation_status import SystemInstallationStatus
from tracardi.service.installation import install_system
from tracardi.config import tracardi, mysql
from tracardi.domain.credentials import Credentials
from tracardi.service.plugin.plugin_install import install_default_plugins
from tracardi.service.storage.mysql.service.database_service import DatabaseService

router = APIRouter()


@router.get("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=SystemInstallationStatus)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """
    return await SystemInstallationStatus.check()


@router.get("/install/plugins", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def install_plugins():
    return await install_default_plugins()


@router.post("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install(credentials: Optional[Credentials]):

    try:
        return await install_system(credentials)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/install/reset/{token}", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def reset_installation(token: str):
    """
    Resets installation
    """
    if tracardi.installation_token and (tracardi.installation_token=='tracardi' or tracardi.installation_token != token):
        raise PermissionError("Installation reset forbidden. Invalid installation token.")

    db = DatabaseService()
    return await db.drop(mysql.mysql_database)

