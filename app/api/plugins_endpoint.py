from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.error_converter import convert_errors
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.service.module_loader import is_coroutine
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageForBulk
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/action/plugins", tags=["action"], include_in_schema=server.expose_gui_api)
async def plugins():
    """
    Returns plugins from database
    """
    return await StorageForBulk().index('action').load()


@router.post("/action/{id}/config/validate", tags=["action"], include_in_schema=server.expose_gui_api)
async def validate_plugin_configuration(id: str, config: dict = None):
    """
    Validates given configuration (obj) of plugin with given ID (str)
    """

    try:
        record = await storage.driver.action.load_by_id(id)

        if record is None:
            raise HTTPException(status_code=404, detail=f"No action plugin for id `{id}`")

        try:
            action_record = FlowActionPluginRecord(**record)
        except ValidationError as e:
            raise HTTPException(status_code=404, detail="Action plugin id `{id}` could not be"
                                                        "validated and mapped into FlowActionPluginRecord object."
                                                        f"Internal error: {str(e)}")

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
