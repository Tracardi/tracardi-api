import logging
from collections import OrderedDict
from typing import Optional

import grpc
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.api.auth.permissions import Permissions
from tracardi.domain.pro_service_form_data import TProMicroserviceCredentials, ProService, ProMicroService
from tracardi.service.plugin.domain.register import Plugin
from tracardi.service.plugin.plugin_install import install_remote_plugin
from tracardi.service.storage.factory import StorageFor

from app.api.domain.credentials import Credentials
from tracardi.config import tracardi
from tracardi.domain.resource import Resource, ResourceRecord
from tracardi.domain.sign_up_data import SignUpData, SignUpRecord
from app.api.proto.tracard_pro_client import TracardiProClient
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.driver import storage
from app.config import server
from tracardi.service.tracardi_http_client import HttpClient

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

tracardi_pro_client = TracardiProClient(host=tracardi.tracardi_pro_host,
                                        port=50000,
                                        secure=False)


@router.get("/tpro/validate", tags=["tpro"], include_in_schema=server.expose_gui_api, response_model=bool)
async def is_token_valid():
    """
    Return None if not configured otherwise returns True if credentials are valid or False.
    """
    try:
        result = await storage.driver.pro.read_pro_service_endpoint()

    except ValidationError as e:
        logger.error(f"Validation error when reading pro service user data: {str(e)}")
        result = None
    except Exception as e:
        logger.error(f"Exception when reading pro service user data: {str(e)}")
        result = None

    if result is None:
        return None

    token = tracardi_pro_client.validate(token=result.token)

    return token is not None


@router.post("/tpro/sign_in", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def tracardi_pro_sign_in(credentials: Credentials):
    """
    Handles signing in to Tracardi PRO service
    """
    try:
        token, host = tracardi_pro_client.sign_in(credentials.username, credentials.password)
        result = await storage.driver.pro.read_pro_service_endpoint()

        # Save locally if data from remote differs with local data.
        if result is None or result.token != token:
            sign_up_record = SignUpRecord(id='0', token=token)
            result = await storage.driver.pro.save_pro_service_endpoint(sign_up_record)

            if result.saved == 0:
                raise ConnectionError("Could not save Tracardi Pro data.")

        return True
    except PermissionError as e:
        msg = "Access denied due to server error:  {}".format(str(e))
        logger.warning(msg, exc_info=True)
        raise HTTPException(detail=msg,
                            status_code=403)  # Must be 403 because 401 logs out gui
    except Exception as e:
        logger.error(str(e), exc_info=True)
        raise HTTPException(detail=str(e), status_code=403)  # Must be 403 because 401 logs out gui


@router.post("/tpro/sign_up", tags=["tpro"], include_in_schema=server.expose_gui_api, response_model=bool)
async def tracardi_pro_sign_up(sign_up_data: SignUpData):
    """
    Handles signing up to Tracardi PRO service
    """
    try:
        # todo save more contact data on Pro server
        token = tracardi_pro_client.sign_up(sign_up_data.username, sign_up_data.password)
        sign_up_record = SignUpRecord(id='0', token=token)
        result = await storage.driver.pro.save_pro_service_endpoint(sign_up_record)

        if result.saved == 0:
            raise ConnectionError("Could not save Tracardi Pro endpoint.")

        return True

    except grpc.RpcError as e:
        raise HTTPException(
            detail="Access denied due to RPC error \"{}\". Error status: {}".format(e.details(), e.code().name),
            status_code=403)  # Must be 403 because 401 logs out gui


@router.get("/tpro/available_services", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_available_services(query: Optional[str] = "", category: Optional[str] = ""):
    """
    Returns available Tracardi PRO services
    """
    try:
        services = await tracardi_pro_client.get_available_services()

        if query:
            query = query.lower()
            result = {key: value for key, value in services['services'].items() if
                      query in value['metadata']['name'].lower() or query in value['metadata']['description'].lower()}
        elif category:
            result = {key: value for key, value in services['services'].items() if
                      category in value['metadata']['tags']}

        else:
            result = services['services']

        services['services'] = OrderedDict(sorted(result.items()))
        return services

    except grpc.RpcError as e:
        # Must be 403 because 401 logs out gui
        raise HTTPException(detail=e.details(), status_code=403 if e.code().name == 'UNAUTHENTICATED' else 500)


@router.get("/tpro/plugin/{module}", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_available_services(module: str):
    """
    Returns available Tracardi PRO services
    """
    try:
        return await tracardi_pro_client.get_plugin(module)

    except grpc.RpcError as e:
        # Must be 403 because 401 logs out gui
        raise HTTPException(detail=e.details(), status_code=403 if e.code().name == 'UNAUTHENTICATED' else 500)


@router.post("/tpro/install", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def save_tracardi_pro_resource(pro: ProService):
    """
    Adds new Tracardi PRO resource
    """
    result = {}

    if 'resource' in pro.service.metadata.submit:
        resource = Resource.from_pro_service(pro)

        def _remove_redundant_data(credentials):
            credentials.pop('name', None)
            credentials.pop('description', None)
            return credentials

        resource.credentials.production = _remove_redundant_data(resource.credentials.production)
        resource.credentials.test = _remove_redundant_data(resource.credentials.test)

        record = ResourceRecord.encode(resource)
        result['resource'] = await StorageFor(record).index().save()
        await storage.driver.resource.refresh()

    if isinstance(pro.plugins, list):
        result['plugin'] = []
        for plugin in pro.plugins:
            plugin = Plugin(**plugin)
            result['plugin'].append(await storage.driver.action.save_plugin(plugin))
        await storage.driver.action.refresh()

    return result


@router.post("/tpro/install/microservice", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def save_tracardi_pro_microservice(pro: ProMicroService):
    """
    Adds new Tracardi PRO resource
    """

    resource = Resource.from_pro_service(pro)

    def _remove_redundant_data(credentials):
        credentials.pop('name', None)
        credentials.pop('description', None)
        return credentials

    resource.credentials.production = _remove_redundant_data(resource.credentials.production)
    resource.credentials.test = _remove_redundant_data(resource.credentials.test)

    production_credentials = TProMicroserviceCredentials(**resource.credentials.production)

    record = ResourceRecord.encode(resource)
    result = await StorageFor(record).index().save()
    await storage.driver.resource.refresh()

    # Create plugin

    if not pro.microservice.service.id or not production_credentials.is_configured():
        raise AssertionError("Microservice Host, Token or Service not configured")

    microservice_plugin_url = f"{production_credentials.url}/plugin/registry?service_id={pro.microservice.service.id}"

    async with HttpClient(3, 200, headers={
        'Authorization': f"Bearer {production_credentials.token}"
    }) as client:
        async with client.get(url=microservice_plugin_url) as response:
            data = await response.json()

            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=data)

            plugin = Plugin(**data)

            plugin.metadata.name = resource.name

            plugin.spec.microservice.service.id = pro.microservice.service.id
            plugin.spec.microservice.service.name = pro.microservice.service.name
            # Set credentials, exclude service data
            plugin.spec.microservice.server.credentials = resource.credentials
            # Configure microservice to be connected with created resource
            plugin.spec.microservice.server.resource.name = resource.name
            plugin.spec.microservice.server.resource.id = resource.id
            # Plugin resources
            plugin.spec.microservice.plugin.resource = pro.microservice.credentials

            await install_remote_plugin(plugin)

    return result
