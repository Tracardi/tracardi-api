from fastapi import APIRouter, Depends

from tracardi.service.storage.mysql.mapping.task_mapping import map_to_task
from tracardi.service.storage.mysql.service.task_service import BackgroundTaskService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.task import Task
from ..service.grouping import get_grouped_result

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

bts = BackgroundTaskService()

@router.get("/tasks", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def load_tasks(query: str = None, start:int = 0, limit: int = 100):

    records = await bts.load_all(search=query, offset=start, limit=limit)
    return get_grouped_result("Tasks", records, map_to_task)

@router.get("/tasks/type/{type}", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def load_tasks_by_type(type: str, query: str = None, start:int = 0, limit: int = 100):

    """Returns tasks of a given type"""

    records = await bts.load_all_by_type(type, search=query, offset=start, limit=limit)
    return get_grouped_result("Tasks", records, map_to_task)


@router.delete("/task/{id}", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def delete_task(id: str):
    return await bts.delete_by_id(id)
    # return await task_db.delete_task(id)


@router.post("/task", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def upsert_task(task: Task):
    return await bts.insert(task)
    # result = await task_db.upsert_task(task)
    # await task_db.refresh()
    # return result
