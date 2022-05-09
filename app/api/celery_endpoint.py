from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.service.celery_worker import run_celery_replay_job, celery

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/import", tags=["job"], include_in_schema=server.expose_gui_api, status_code=201)
async def run_import_job():
    job = run_celery_replay_job.delay()
    return {
        "job": str(job.id)
    }


@router.get("/import/status/{task_id}")
def get_status(job_id):
    job_result = AsyncResult(job_id, app=celery)
    result = {
        "job": job_result.id,
        "status": job_result.status,
        "result": job_result.result
    }
    return result

