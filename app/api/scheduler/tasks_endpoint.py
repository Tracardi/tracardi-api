import logging
import time

from fastapi import APIRouter, Depends

from tracardi.domain.task import Task
from tracardi.service.storage.factory import storage, StorageForBulk

from app.api.auth.authentication import get_current_user

logger = logging.getLogger('app.api.scheduler.tasks_endpoint')
logger.setLevel(logging.INFO)


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/tasks/run", tags=["tasks"])
async def run_tasks():
    now = time.time()

    query = {
        "size": 100,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "timestamp": {
                                "lte": now
                            }
                        }
                    },
                    {
                        "term": {
                            "status": {
                                "value": "pending"
                            }
                        }
                    }
                ]
            }
        }
    }
    print(query)
    tasks = await storage('task').filter(query)
    logger.info("Found {} task to run.".format(len(tasks)))
    event_tasks = []
    bulk_tasks = []
    for task in tasks:
        print(now, task)
        task = Task(**task)

        task_coroutine = task.run()
        event_tasks.append(task_coroutine)
        task.status = 'running'
        bulk_tasks.append(task)

    result = await StorageForBulk(bulk_tasks).index('task').save()

    bulk_tasks = []
    for task in event_tasks:

        result, _task = await task
        if _task.status == 'running':
            _task.status = 'done'
        print('_task', _task)
        bulk_tasks.append(_task)

    return await StorageForBulk(bulk_tasks).index('task').save()
