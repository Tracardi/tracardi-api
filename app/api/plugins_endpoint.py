from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.error_converter import convert_errors
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.service.module_loader import is_coroutine
from tracardi.service.storage.driver import storage
from fastapi.encoders import jsonable_encoder
from tracardi.service.module_loader import import_package, load_callable

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/plugin/{module}/{endpoint_function}", tags=["action"], include_in_schema=server.expose_gui_api)
async def get_data_for_plugin(module: str, endpoint_function: str, request: Request):
    """
    Calls helper method from Endpoint class in plugin's module
    """

    try:
        if not module.startswith('tracardi.process_engine'):
            raise HTTPException(status_code=404, detail="This is not helper endpoint.")

        module = import_package(module)
        endpoint_module = load_callable(module, 'Endpoint')
        function_to_call = getattr(endpoint_module, endpoint_function)

        if is_coroutine(function_to_call):
            return await function_to_call(await request.json())
        return function_to_call(await request.json())

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
    except HTTPException as e:
        raise e
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/action/plugins", tags=["action"], include_in_schema=server.expose_gui_api)
async def plugins():
    """
    Returns plugins from database
    """
    return await storage.driver.action.load_all()


@router.post("/plugin/{plugin_id}/config/validate", tags=["action"], include_in_schema=server.expose_gui_api)
async def validate_plugin_configuration(plugin_id: str,
                                        action_id: Optional[str] = "",
                                        service_id: Optional[str] = "",
                                        config: dict = None,
                                        credentials: dict = None):
    """
    Validates given configuration (obj) of plugin with given ID (str)
    """

    try:
        record = await storage.driver.action.load_by_id(plugin_id)

        if record is None:
            raise HTTPException(status_code=404, detail=f"No action plugin for id `{plugin_id}`")

        try:
            action_record = FlowActionPluginRecord(**record)
        except ValidationError as e:
            raise HTTPException(status_code=404, detail="Action plugin id `{id}` could not be"
                                                        "validated and mapped into FlowActionPluginRecord object."
                                                        f"Internal error: {str(e)}")
        # todo move to action_record class

        if action_record.plugin.metadata.remote is True:
            # Run validation thru remote validator not local microservice plugin

            microservice = action_record.plugin.spec.microservice
            production_credentials = microservice.server.credentials.production
            microservice_url = f"{production_credentials['url']}/plugin/validate" \
                               f"?service_id={service_id}" \
                               f"&action_id={action_id}"

            async with aiohttp.ClientSession(headers={
                'X-Token': production_credentials['token']
            }) as client:
                async with client.post(
                        url=microservice_url,
                        json={
                            "config": config,
                            "credentials": credentials
                        }) as remote_response:
                    return JSONResponse(
                        status_code=remote_response.status,
                        content=jsonable_encoder(await remote_response.json())
                    )

        else:

            # Run validation locally

            validate = action_record.get_validator()

            if config is None:
                raise HTTPException(status_code=404, detail="No validate function provided. "
                                                            "Could not validate on server side.")

            if is_coroutine(validate):
                return await validate(config)
            return validate(config)

    except HTTPException as e:
        raise e
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
