from com_tracardi.scheduler.rq_clinet import RQClient
from fastapi import APIRouter, Depends

from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/scheduler/jobs",
            tags=["scheduler"],
            include_in_schema=server.expose_gui_api)
async def get_scheduled_jobs():
    schedule = RQClient()
    return [{"time": scheduled_time, "job_id": job.id} for job, scheduled_time in schedule.list()]
