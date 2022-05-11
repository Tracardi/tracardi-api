from fastapi import APIRouter, HTTPException, Depends

from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from tracardi.exceptions.exception import StorageException
from tracardi.domain.task import Task


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/tasks", tags=["task"], include_in_schema=server.expose_gui_api)
async def load_tasks(limit: int = 100):
    try:
        result = await storage.driver.task.load_tasks(limit)
        return {
            "grouped": {
                "Imports": result
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/task/{id}", tags=["task"], include_in_schema=server.expose_gui_api)
async def delete_task(id: str):
    try:
        return await storage.driver.task.delete_task(id)

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task", tags=["task"], include_in_schema=server.expose_gui_api)
async def upsert_task(task: Task):
    try:
        return await storage.driver.task.upsert_task(task)

    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task/{id}/progress", tags=["task"], include_in_schema=server.expose_gui_api)
async def get_task_progress(id: str):
    try:
        result = await storage.driver.task.get_progress(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Task {id} not found.")
        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
