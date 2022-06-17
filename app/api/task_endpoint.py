from fastapi import APIRouter, HTTPException, Depends

from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from tracardi.exceptions.exception import StorageException
from tracardi.domain.task import Task


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "data_admin"]))]
)


@router.get("/tasks", tags=["task"], include_in_schema=server.expose_gui_api)
async def load_tasks(query: str = None, limit: int = 20):
    try:
        if not query:
            query = {
                "match_all": {}
            }
        else:
            query = {
                "wildcard": {
                    "name": f"*{query}*"
                }
            }

        result = await storage.driver.task.load_tasks(query, limit=limit)
        return {
            "grouped": {
                "Imports": list(result)
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
