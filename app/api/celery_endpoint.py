from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.celery.celery_worker import run_celery_replay_job, celery

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/import", tags=["task"], include_in_schema=server.expose_gui_api, status_code=201)
async def run_import_job():
    task = run_celery_replay_job.delay()
    return {
        "task": str(task.id)
    }


@router.get("/import/status/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    result = {
        "task": task_result.id,
        "status": task_result.status,
        "result": task_result.result
    }
    return result

