from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from tracardi.config import mysql
from tracardi.context import get_context
from tracardi.service.plugin.plugin_install import install_default_plugins
from tracardi.service.storage.index import Resource
from tracardi.service.storage.mysql.service.database_service import DatabaseService
from tracardi.config import tracardi
from .auth.permissions import Permissions
from tracardi.service.storage.elastic.interface.gui.storage import reindex, remove_index, list_indices, remove_template, \
    remove_alias

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["maintainer"]))]
)


@router.get("/install/reset/{token}", tags=["maintenance"], include_in_schema=tracardi.expose_gui_api)
async def reset_installation(token: str):
    """
    This is the full reset  of the installation
    """

    if tracardi.installation_token and (
            tracardi.installation_token == 'tracardi' or tracardi.installation_token != token):
        raise PermissionError("Installation reset forbidden. Invalid installation token.")

    db_version = tracardi.version.db_version
    tenant = get_context().tenant

    indices = await list_indices()

    # Test
    to_delete = [index for index in indices if index.startswith(
        f"{db_version}.{tenant}.tracardi-"
    )]

    # Production
    for index in indices:
        if index.startswith(f"prod-{db_version}.{tenant}.tracardi-"):
            to_delete.append(index)

    result = {}
    for alias in to_delete:
        try:
            result[alias] = await remove_index(alias)
        except Exception:
            pass

    # Remaining aliases, templates, etc

    resource = Resource()
    aliases = resource.list_aliases()
    indices = resource.list_indices()
    templates = resource.list_templates()

    # Production
    for index in indices.copy():
        indices.add(f"prod-{index}")

    for alias in aliases.copy():
        aliases.add(f"prod-{alias}")

    for template in templates.copy():
        templates.add(f"prod-{template}")

    for index in indices:
        try:
            result[index] = await remove_index(index)
        except Exception:
            pass

    for alias in aliases:
        try:
            result[alias] = await remove_alias(alias)
        except Exception:
            pass

    for template in templates:
        try:
            result[template] = await remove_template(template)
        except Exception:
            pass
    db = DatabaseService()
    await db.drop(mysql.mysql_database)

    return result


@router.get("/install/plugins", tags=["maintenance"], include_in_schema=tracardi.expose_gui_api)
async def install_plugins():
    return await install_default_plugins()


@router.get("/reindex/{source}/{destination}", tags=["maintenance"], include_in_schema=tracardi.expose_gui_api)
async def reindex_data(source: str, destination: str, wait_for_completion: bool = True):
    """
    Copies data from one index to another.
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This operation is not allowed for multi-tenant server.")

    return await reindex(source, destination, wait_for_completion)


@router.delete("/indices", tags=["maintenance"], include_in_schema=tracardi.expose_gui_api)
async def delete_old_indices(db_version: str, codename: Optional[str] = None):
    if db_version == tracardi.version.db_version:
        raise HTTPException(status_code=409, detail="You cannot delete indices that are currently used.")

    indices = await list_indices()

    # Test
    to_delete = [index for index in indices if index.startswith(
        f"{db_version}.{codename}.tracardi-"
    )]

    # Production
    for index in indices:
        if index.startswith(f"prod-{db_version}.{codename}.tracardi-"):
            to_delete.append(index)

    result = {}
    for alias in to_delete:
        result[alias] = await remove_index(alias)

    return result
