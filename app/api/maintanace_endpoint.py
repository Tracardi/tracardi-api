from fastapi import APIRouter, Depends

from tracardi.config import mysql
from tracardi.service.plugin.plugin_install import install_default_plugins
from tracardi.service.storage.mysql.service.database_service import DatabaseService
from tracardi.config import tracardi
from .auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["maintainer"]))]
)

@router.get("/install/reset/{token}", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def reset_installation(token: str):
    """
    Resets installation
    """
    if tracardi.installation_token and (tracardi.installation_token=='tracardi' or tracardi.installation_token != token):
        raise PermissionError("Installation reset forbidden. Invalid installation token.")

    db = DatabaseService()
    return await db.drop(mysql.mysql_database)


@router.get("/install/plugins", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install_plugins():
    return await install_default_plugins()