from fastapi import APIRouter, HTTPException, Depends

from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from tracardi.exceptions.exception import StorageException
from tracardi.domain.batch import Batch
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


@router.get("/batch/{id}", tags=["batch"], include_in_schema=server.expose_gui_api)
async def get_batch_by_id(id: str):
    try:
        result = await storage.driver.batch.load(id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"No batch found for id {id}")

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", tags=["batch"], include_in_schema=server.expose_gui_api)
async def add_batch(batch: Batch):
    try:
        module = batch.module.split(".")
        package = import_package(".".join(module[:-1]))
        batch_class = getattr(package, module[-1])
        batch_class.config_class(**batch.config)
        result = await storage.driver.batch.add_batch(batch)
        await storage.driver.batch.refresh()
        return result

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/batch/{id}", tags=["batch"], include_in_schema=server.expose_gui_api)
async def delete_batch(id: str):
    try:
        result = await storage.driver.batch.delete(id)
        await storage.driver.batch.refresh()
        return result

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/batches", tags=["batch"], include_in_schema=server.expose_gui_api)
async def load_batches(limit: int = 100, query: str = None):
    try:
        result = await storage.driver.batch.load_batches(limit, query)
        return {"grouped": {"General": result}} if result else {}

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/run/{id}", tags=["batch"], include_in_schema=server.expose_gui_api)
async def run_batch(id: str, debug: bool = True):
    try:
        batch_object = await storage.driver.batch.load(id)
        if batch_object is None:
            raise HTTPException(status_code=404, detail=f"No batch found for id {id}")

        if batch_object.enabled is False:
            raise HTTPException(status_code=409, detail=f"Selected batch is disabled")

        module = batch_object.module.split(".")
        package = import_package(".".join(module[:-1]))

        batch = getattr(package, module[-1])(debug)

        batch.run(batch_object.config)

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/batches/types", tags=["batch"], include_in_schema=server.expose_gui_api)
async def get_batch_types():
    return get_batches()


@router.get("/batch/form/{module}", tags=["batch"], include_in_schema=server.expose_gui_api)
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


@router.post("/batch/validate-config/{module}", tags=["batch"], include_in_schema=server.expose_gui_api)
async def validate_batch_config(module: str, config: dict):
    try:
        if module:
            module = module.split(".")
            package = import_package(".".join(module[:-1]))
            batch_class = getattr(package, module[-1])
            batch_class.config_class(**config)
        else:
            raise HTTPException(status_code=422, detail="No batch type selected")

    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(convert_errors(e))
        )
