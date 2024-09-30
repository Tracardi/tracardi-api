from collections import OrderedDict
from typing import Optional

from com_tracardi.pro.db.plugins import plugins
from tracardi.service.license import License
from tracardi.service.storage.mysql.interface import resource_dao
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.auth.permissions import Permissions
from tracardi.domain.pro_service_form_data import ProService
from tracardi.service.plugin.domain.register import Plugin
from tracardi.service.plugin.plugin_install import install_plugin
from tracardi.domain.resource import Resource
from tracardi.exceptions.log_handler import get_logger
from tracardi.config import tracardi

if License.has_license():
    from com_tracardi.pro.service.tracardi_pro import get_available_services

logger = get_logger(__name__)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


async def _store_resource_record(data: Resource):
    return await resource_dao.insert_resource(data)


@router.get("/tpro/validate", tags=["tpro"], include_in_schema=tracardi.expose_gui_api)
async def is_token_valid() -> Optional[bool]:
    """
    Return None if not configured otherwise returns True if credentials are valid or False.
    """
    return True


@router.get("/tpro/available_services", tags=["tpro"], include_in_schema=tracardi.expose_gui_api)
async def get_extension_services(query: Optional[str] = "", category: Optional[str] = ""):
    """
    Returns available Tracardi PRO services
    """
    if License.has_license():
        services = get_available_services(query, category,
                                          version=tracardi.image_tag if tracardi.image_tag != 'n/a' else "1.0.0")
        return {
            "services": OrderedDict(sorted(services.items()))
        }

    return {
        "services": {}
    }


@router.get("/tpro/plugin/{module}", tags=["tpro"], include_in_schema=tracardi.expose_gui_api)
async def get_available_plugin_modules(module: str):
    """
    Returns available Tracardi PRO services
    """

    if module not in plugins:
        raise HTTPException(
            detail=f"Plugin `{module}` is not available.",
            status_code=403
        )

    form = plugins[module]['form'] if 'form' in plugins[module] else {}
    init = plugins[module]['init'] if 'init' in plugins[module] else {}

    return dict(
        init=init,
        form=form.model_dump(mode='json') if isinstance(form, BaseModel) else {}
    )


@router.post("/tpro/install", tags=["tpro"], include_in_schema=tracardi.expose_gui_api)
async def save_tracardi_pro_resource(pro: ProService):
    """
    Adds new Tracardi PRO resource
    """
    result = {}

    # Add resource

    if 'resource' in pro.service.metadata.submit:
        resource = Resource.from_pro_service(pro)

        def _remove_redundant_data(credentials):
            credentials.pop('name', None)
            credentials.pop('description', None)
            return credentials

        resource.credentials.production = _remove_redundant_data(resource.credentials.production)
        resource.credentials.test = _remove_redundant_data(resource.credentials.test)

        result['resource'] = await _store_resource_record(resource)

    # Add plugins

    if isinstance(pro.plugins, list):
        result['plugin'] = []
        for plugin in pro.plugins:
            plugin = Plugin(**plugin)
            response = await install_plugin(plugin.spec.module)
            result['plugin'].append(response)

    return result
