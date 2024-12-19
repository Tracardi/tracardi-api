from json import JSONDecodeError
from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from app.service.error_converter import convert_errors
from tracardi.domain.config_validation_payload import ConfigValidationPayload
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.module_loader import is_coroutine
from fastapi.encoders import jsonable_encoder
from tracardi.service.module_loader import import_package, load_callable
from tracardi.service.storage.mysql.mapping.plugin_mapping import map_to_flow_action_plugin
from tracardi.service.storage.mysql.service.action_plugin_service import ActionPluginService

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

logger = get_logger(__name__)

@router.post("/plugin/{module}/{endpoint_function}", tags=["action"], include_in_schema=tracardi.expose_gui_api)
async def get_data_for_plugin(module: str, endpoint_function: str, request: Request):
    """
    Calls helper method from Endpoint class in plugin's module
    """

    try:
        if not module.startswith('tracardi.process_engine') and not module.startswith('com_tracardi.action'):
            raise HTTPException(status_code=404, detail="This is not helper endpoint.")

        module = import_package(module)
        endpoint_module = load_callable(module, 'Endpoint')
        function_to_call = getattr(endpoint_module, endpoint_function)

        try:
            body = await request.json()
        except JSONDecodeError:
            body = {}

        if is_coroutine(function_to_call):
            return await function_to_call(body)
        return function_to_call(body)

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/plugin/{plugin_id}/config/validate", tags=["action"], include_in_schema=tracardi.expose_gui_api)
async def validate_plugin_configuration(plugin_id: str,
                                        action_id: Optional[str] = "",
                                        service_id: Optional[str] = "",
                                        config: ConfigValidationPayload = None):
    # """
    # Validates given configuration (obj) of plugin with given ID (str)
    # """

    # try:

        aps = ActionPluginService()
        record =await aps.load_by_id(plugin_id)

        if record is None:
            raise HTTPException(status_code=404, detail=f"No action plugin for id `{plugin_id}`")

        plugin: FlowActionPlugin = record.map_to_object(map_to_flow_action_plugin)

        # todo move to action_record class

        if plugin.plugin.metadata.remote is True:
            # Run validation thru remote validator not local microservice plugin

            microservice = plugin.plugin.spec.microservice
            production_credentials = microservice.server.credentials.production
            microservice_url = f"{production_credentials['url']}/plugin/validate" \
                               f"?service_id={service_id}" \
                               f"&action_id={action_id}"

            async with aiohttp.ClientSession(headers={
                'Authorization': f"Bearer {production_credentials['token']}"
            }) as client:
                payload= {'config': {'attributes': {
                    "src": "xxx"
                }, 'content': 'sadsd'},
                 'credentials': {'uix_mf_source': 'http://localhost'}}
                payload = config.model_dump(mode='json')
                async with client.post(
                        url=microservice_url,
                        json=payload) as remote_response:

                    return JSONResponse(
                        status_code=remote_response.status,
                        content=jsonable_encoder(await remote_response.json())
                    )

        else:

            # Run validation locally

            validate = plugin.get_validator()

            if config.config is None:
                raise HTTPException(status_code=404, detail="No validate function provided. "
                                                            "Could not validate on server side.")

            if is_coroutine(validate):
                return await validate(config.config)
            return validate(config.config)

    # except HTTPException as e:
    #     logger.error(str(e))
    #     raise e
    # except AttributeError as e  :
    #     raise HTTPException(status_code=404, detail=str(e))
    # except ValidationError as e:
    #     return JSONResponse(
    #         status_code=422,
    #         content=jsonable_encoder(convert_errors(e))
    #     )
