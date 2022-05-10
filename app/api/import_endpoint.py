from fastapi import APIRouter, HTTPException, Depends

from tracardi.service.storage.driver import storage
from worker.celery_worker import celery
from .auth.permissions import Permissions
from ..config import server
from tracardi.exceptions.exception import StorageException
from tracardi.domain.import_config import ImportConfig
from tracardi.service.import_types import get_import_types
from tracardi.service.module_loader import import_package
from pydantic import ValidationError
from celery.result import AsyncResult
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.service.error_converter import convert_errors

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/import/status/{task_id}", tags=["import"], include_in_schema=server.expose_gui_api)
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    result = {
        "task": task_result.id,
        "status": task_result.status,
        "result": task_result.result
    }
    return result


@router.get("/import/types", tags=["import"], include_in_schema=server.expose_gui_api)
async def load_import_types():
    return get_import_types()


@router.get("/import/{import_id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def get_import_by_id(import_id: str):
    try:
        result = await storage.driver.import_config.load(import_id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"No import configuration found for id {import_id}")

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import", tags=["import"], include_in_schema=server.expose_gui_api)
async def add_import_config(import_configuration: dict):
    try:
        import_configuration = ImportConfig(**import_configuration)
        module = import_configuration.module.split(".")
        package = import_package(".".join(module[:-1]))
        import_processor = getattr(package, module[-1])

        # Validate data with the configuration model
        import_processor.config_model(**import_configuration.config)

        # Safe configuration
        result = await storage.driver.import_config.save(import_configuration)
        await storage.driver.import_config.refresh()
        return result

    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/import/{import_id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def delete_import_configuration(import_id: str):
    try:
        result = await storage.driver.import_config.delete(import_id)
        await storage.driver.import_config.refresh()
        return result

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/imports", tags=["import"], include_in_schema=server.expose_gui_api)
async def load_all_imports(limit: int = 100, query: str = None):
    try:
        result = await storage.driver.import_config.load_all(limit, query)
        return {"grouped": {"General": result}} if result else {}

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/run/{import_id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def run_import(import_id: str, debug: bool = True):
    try:

        import_configuration = await storage.driver.import_config.load(import_id)
        if import_configuration is None:
            raise HTTPException(status_code=404, detail=f"No import source configuration found for id {import_id}")

        if import_configuration.enabled is False:
            raise HTTPException(status_code=409, detail=f"Selected import source is disabled")

        module = import_configuration.module.split(".")
        package = import_package(".".join(module[:-1]))

        importer = getattr(package, module[-1])(debug)

        await importer.run(import_configuration.config)

        return {
            "task": {
                "id": 1
            }
        }

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/import/form/{module}", tags=["import"], include_in_schema=server.expose_gui_api)
async def get_import_configuration_form(module: str):
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
