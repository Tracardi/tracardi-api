from fastapi import APIRouter, Depends

from tracardi.service.storage.driver.elastic import task as task_db
from .auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.task import Task

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/tasks", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def load_tasks(query: str = None, limit: int = 50):
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

    result = await task_db.load_tasks(query, limit=limit)
    return {
        "grouped": {
            "Tasks": list(result)
        }
    }


@router.get("/tasks/type/{type}", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def load_tasks_by_type(type: str, query: str = None, limit: int = 50):

    """Returns tasks of a given type"""

    body = {
        "bool": {
            "must": [
                {
                    "term": {
                        "type": type
                    }
                }
            ]
        }
    }

    if query:
        body['bool']['must'].append({
            "wildcard": {
                "name": f"*{query}*"
            }
        })

    result = await task_db.load_tasks(body, limit=limit)

    return {
        "grouped": {
            "Tasks": list(result)
        }
    }


@router.delete("/task/{id}", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def delete_task(id: str):
    return await task_db.delete_task(id)


@router.post("/task", tags=["task"], include_in_schema=tracardi.expose_gui_api)
async def upsert_task(task: Task):
    result = await task_db.upsert_task(task)
    await task_db.refresh()
    return result
