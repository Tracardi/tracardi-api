from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from tracardi.process_engine.importing.importer import Importer
from tracardi.service.storage.mysql.mapping.import_mapping import map_to_import_config
from tracardi.service.storage.mysql.mapping.task_mapping import map_to_task
from tracardi.service.storage.mysql.service.import_service import ImportService
from tracardi.service.storage.mysql.service.task_service import BackgroundTaskService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.import_config import ImportConfig
from tracardi.service.setup.setup_import_types import get_import_types
from tracardi.service.module_loader import import_package
from pydantic import ValidationError
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.service.error_converter import convert_errors
from ..service.grouping import get_grouped_result

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


async def _load_by_id(import_id: str) -> Optional[ImportConfig]:
    ics = ImportService()
    record = await ics.load_by_id(import_id)

    if not record.exists():
        raise HTTPException(status_code=404, detail=f"No import configuration found for id {import_id}")

    return record.map_to_object(map_to_import_config)


@router.get("/import/{import_id}/run", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def run_import(import_id: str, name: str = None, debug: bool = True):

    """
    Takes import id and returns worker task id.
    """

    try:

        import_configuration = await _load_by_id(import_id)

        if import_configuration.enabled is False:
            raise HTTPException(status_code=409, 
                                detail="Selected import source is disabled")

        module = import_configuration.module.split(".")
        package = import_package(".".join(module[:-1]))

        importer: Importer = getattr(package, module[-1])(debug)

        await importer.run(name, import_configuration)

        return None

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/import/task/{task_id}/status", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def get_status(task_id):
    """
    Takes worker task id and returns current status
    """

    bts = BackgroundTaskService()
    record = await bts.load_by_id(task_id)

    if not record.exists():
        return {
            "id": task_id,
            "status": "none",
            "progress": 0,
            "message": None
        }

    task = record.map_to_object(map_to_task)
    result = {
        "id": task.id,
        "status": task.status,
        "progress": task.progress,
        "message": task.message
    }
    return result


# Tracardi endpoints

@router.get("/import/types", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def load_import_types():

    """
    Returns available import types.
    """

    return get_import_types()


@router.get("/import/{import_id}", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def get_import_by_id(import_id: str):

    """
    Returns import configuration.
    """
    return await _load_by_id(import_id)

@router.post("/import", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def save_import_config(import_configuration: dict):

    """
    Adds new import configurations.
    """

    try:
        import_configuration = ImportConfig(**import_configuration)
        module = import_configuration.module.split(".")
        package = import_package(".".join(module[:-1]))
        import_processor = getattr(package, module[-1])

        # Validate data with the configuration model
        import_processor.config_model(**import_configuration.config)

        print(import_configuration)

        # Safe configuration
        ics = ImportService()
        return await ics.insert(import_configuration)

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )


@router.delete("/import/{import_id}", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def delete_import_configuration(import_id: str):

    """
    Deletes import configuration
    """

    ics = ImportService()
    return await ics.delete_by_id(import_id)


@router.get("/imports", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def get_all_imports(start:int = 0,  limit: int = 100, query: str = None):

    """
    Returns all imports.
    """
    ics = ImportService()
    records = await ics.load_all(search=query, offset=start, limit=limit)
    return get_grouped_result("Imports", records, map_to_import_config)


@router.get("/import/form/{module}", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def get_import_configuration_form(module: str):

    """
    Returns import configuration form for selected import type
    """

    try:
        module = module.split(".")
        package = import_package(".".join(module[:-1]))
        import_configuration = getattr(package, module[-1])
        return {
            "form": import_configuration.form,
            "init": import_configuration.init
        }

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
