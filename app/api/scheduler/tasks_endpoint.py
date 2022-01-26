import asyncio
import logging
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from app.api.track.service.tracker import track_event
from app.config import server
from tracardi.config import tracardi
from tracardi.domain.task import Task
from tracardi.service.network import local_ip
from tracardi.service.storage.driver import storage
from app.api.auth.authentication import get_current_user

logger = logging.getLogger('app.api.scheduler.tasks_endpoint')
logger.setLevel(tracardi.logging_level)

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/tasks", tags=["tasks"], include_in_schema=server.expose_gui_api)
async def add_tasks(tasks: List[Task]):
    return await storage.driver.task.save_tasks(tasks)


@router.get("/tasks/page/{page}", tags=["tasks"], include_in_schema=server.expose_gui_api)
@router.get("/tasks", tags=["tasks"], include_in_schema=server.expose_gui_api)
async def all_tasks(page: Optional[int] = None):
    try:
        if page is None:
            page = 0
            page_size = 100
        else:
            page_size = server.page_size
        start = page * page_size
        limit = page_size
        result = await storage.driver.task.load_all(start, limit)
        return {
            "total": result.total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/run", tags=["tasks"], include_in_schema=server.expose_gui_api)
async def run_tasks():
    def run(task: Task):
        tracker_payload = task.event.to_tracker_payload()

        async def _task():
            try:
                return await track_event(tracker_payload, ip=local_ip), task
            except Exception as e:
                logger.error("Scheduled task error: ".format(str(e)))
                task.status = 'error'
                return None, task

        return asyncio.create_task(_task())

    tasks = await storage.driver.task.load_pending_tasks()

    logger.info("Found {} task to run.".format(len(tasks)))
    event_tasks = []
    bulk_tasks = []
    for task in tasks:
        task = Task(**task)
        task_coroutine = run(task)
        event_tasks.append(task_coroutine)
        task.status = 'running'
        bulk_tasks.append(task)

    result = await storage.driver.task.save_tasks(bulk_tasks)

    bulk_tasks = []
    for task in event_tasks:
        # todo check for errors
        result, _task = await task
        if _task.status == 'running':
            _task.status = 'done'

        bulk_tasks.append(_task)

    return await storage.driver.task.save_tasks(bulk_tasks)
