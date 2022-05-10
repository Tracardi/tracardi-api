from fastapi import APIRouter, HTTPException, Depends

from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from tracardi.exceptions.exception import StorageException
from tracardi.domain.import_config import ImportConfig
from tracardi.service.batches import get_batches
from tracardi.service.module_loader import import_package, is_coroutine
from pydantic import ValidationError
from tracardi.service.storage.redis_client import RedisClient
from uuid import uuid4
import asyncio
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.service.error_converter import convert_errors

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/import/types", tags=["import"], include_in_schema=server.expose_gui_api)
async def get_batch_types():
    return get_batches()


@router.get("/import/{id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def get_batch_by_id(id: str):
    try:
        result = await storage.driver.import_config.load(id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"No batch found for id {id}")

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


@router.delete("/import/{id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def delete_batch(id: str):
    try:
        result = await storage.driver.import_config.delete(id)
        await storage.driver.import_config.refresh()
        return result

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/imports", tags=["import"], include_in_schema=server.expose_gui_api)
async def load_batches(limit: int = 100, query: str = None):
    try:
        result = await storage.driver.import_config.load_all(limit, query)
        return {"grouped": {"General": result}} if result else {}

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/run/{id}", tags=["import"], include_in_schema=server.expose_gui_api)
async def run_import(id: str, debug: bool = True):
    try:

        import_configuration = await storage.driver.import_config.load(id)
        if import_configuration is None:
            raise HTTPException(status_code=404, detail=f"No import source configuration found for id {id}")

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
async def get_batch_form(module: str):
    try:
        module = module.split(".")
        package = import_package(".".join(module[:-1]))
        batch_class = getattr(package, module[-1])
        return {
            "form": batch_class.form,
            "init": batch_class.init
        }

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/import/validate-config/{module}", tags=["import"], include_in_schema=server.expose_gui_api)
async def validate_batch_config(module: str, config: dict):
    try:
        if module:
            module = module.split(".")
            package = import_package(".".join(module[:-1]))
            import_class = getattr(package, module[-1])
            import_class.config_model(**config)
        else:
            raise HTTPException(status_code=422, detail="No batch type selected")

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
