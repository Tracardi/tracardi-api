from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from starlette.responses import JSONResponse

from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageForBulk
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/action/plugins", tags=["action"], include_in_schema=server.expose_gui_api)
async def plugins():
    return await StorageForBulk().index('action').load()


@router.post("/action/{id}/config/validate", tags=["action"], include_in_schema=server.expose_gui_api)
async def validate_plugin_configuration(id: str, config: dict = None):
    try:
        record = await storage.driver.action.load_by_id(id)
        action_record = FlowActionPluginRecord(**record)
        validate = action_record.get_validator()
        if config is None:
            raise ValueError("No configuration provided. Nothing to validate.")
        return validate(config)
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        response = {}
        for error in e.errors():
            if 'loc' not in error or 'msg' not in error:
                continue
            for field in error['loc']:
                # One field at a time. This is ok to override field errors.
                response[field] = error['msg'].capitalize()
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(response)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
