from fastapi import APIRouter, HTTPException, Depends
from tracardi.service.storage.driver.elastic import import_config as import_config_db
from tracardi.worker.celery_worker import celery
from .auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.import_config import ImportConfig
from tracardi.service.setup.setup_import_types import get_import_types
from tracardi.service.module_loader import import_package
from pydantic import ValidationError
from celery.result import AsyncResult
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.service.error_converter import convert_errors

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


# Celery worker endpoints

@router.get("/import/{import_id}/run", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def run_import(import_id: str, name: str = None, debug: bool = True):

    """
    Takes import id and returns worker task id.
    """

    try:

        import_configuration = await import_config_db.load(import_id)
        if import_configuration is None:
            raise HTTPException(status_code=404, 
                                detail=f"No import source configuration found for id {import_id}")

        if import_configuration.enabled is False:
            raise HTTPException(status_code=409, 
                                detail="Selected import source is disabled")

        module = import_configuration.module.split(".")
        package = import_package(".".join(module[:-1]))

        importer = getattr(package, module[-1])(debug)

        task_id, celery_task_id = await importer.run(name, import_configuration)

        return {
            "id": task_id,
            "task_id": celery_task_id
        }

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/import/task/{task_id}/status", tags=["import"], include_in_schema=tracardi.expose_gui_api)
def get_status(task_id):
    """
    Takes worker task id and returns current status
    """
    task_result = AsyncResult(task_id, app=celery)
    result = {
        "id": task_result.id,
        "status": task_result.status,
        "progress": task_result.result
    }
    return result


@router.delete("/import/task/{task_id}", tags=["import"], include_in_schema=tracardi.expose_gui_api)
def delete_import_task(task_id):

    """
    Takes worker task id and cancels task
    """

    return celery.control.revoke(task_id, terminate=True)


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

    result = await import_config_db.load(import_id)
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No import configuration found for id {import_id}")


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

        # Safe configuration
        result = await import_config_db.save(import_configuration)
        await import_config_db.refresh()
        return result

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

    result = await import_config_db.delete(import_id)
    await import_config_db.refresh()
    return result


@router.get("/imports", tags=["import"], include_in_schema=tracardi.expose_gui_api)
async def get_all_imports(limit: int = 50, query: str = None):

    """
    Returns all imports.
    """

    result = await import_config_db.load_all(limit, query)
    return {"grouped": {"General": result}} if result else {}


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
