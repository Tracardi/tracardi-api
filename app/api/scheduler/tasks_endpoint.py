import logging
from fastapi import APIRouter, Depends, HTTPException
from tracardi.domain.task import Task
from tracardi.service.storage.driver import storage
from app.api.auth.authentication import get_current_user

logger = logging.getLogger('app.api.scheduler.tasks_endpoint')
logger.setLevel(logging.INFO)


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/tasks", tags=["tasks"])
async def all_tasks():
    try:
        result = await storage.driver.task.load_all()
        return {
            "total": result.total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/run", tags=["tasks"])
async def run_tasks():
    tasks = await storage.driver.task.load_pending_tasks()

    logger.info("Found {} task to run.".format(len(tasks)))
    event_tasks = []
    bulk_tasks = []
    for task in tasks:
        task = Task(**task)

        task_coroutine = task.run()
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
        print('_task', _task)
        bulk_tasks.append(_task)

    return await storage.driver.task.save_tasks(bulk_tasks)
