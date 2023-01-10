import logging
from datetime import datetime, timedelta
from typing import Union, Optional

import rq

from com_tracardi.scheduler.rq_clinet import RQClient
from fastapi import APIRouter, Depends, Request, HTTPException, status

from com_tracardi.scheduler.tracker import schedule_track
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.domain.storage_record import StorageRecords
from tracardi.exceptions.exception import UnauthorizedException, FieldTypeConflictException, EventValidationException, \
    TracardiException
from tracardi.exceptions.log_handler import log_handler
from .auth.permissions import Permissions
from .domain.schedule import Job
from .track.service.ip_address import get_ip_address
from ..config import server
from ..service.grouping import group_records

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/scheduler/jobs",
            tags=["scheduler"],
            include_in_schema=server.expose_gui_api)
async def get_scheduled_jobs(query: Optional[str] = None):
    schedule = RQClient()
    records = [{
        "_id": job.id,
        "_index": "scheduler",
        "_source": {
            "time": scheduled_time,
            "job_id": job.id,
            "meta": job.meta,
            "name": job.meta.get("name", "n/a"),
            "description": job.meta.get("description", ""),
            "tags": ["General", job.origin]
        }
    } for job, scheduled_time in schedule.list()]

    sr = StorageRecords()
    sr.set_data(records, total=len(records))

    return group_records(sr, query, group_by='tags', search_by='name', sort_by='name')


@router.get("/scheduler/job/{job_id}",
            tags=["scheduler"],
            include_in_schema=server.expose_gui_api)
async def schedule_job(job_id: str):
    schedule = RQClient()
    job = schedule.get_job(job_id)
    result = job.to_dict(include_meta=False)

    if 'data' in result:
        del result['data']
    if 'result' in result:
        del result['result']

    result['meta'] = job.meta
    return result


@router.delete("/scheduler/job/{job_id}",
               tags=["scheduler"],
               include_in_schema=server.expose_gui_api)
async def schedule_job(job_id: str):
    schedule = RQClient()
    schedule.cancel(job_id)


@router.post("/scheduler/job",
             tags=["scheduler"],
             include_in_schema=server.expose_gui_api)
async def schedule_job(
        job: Job,
        request: Request):
    try:

        if isinstance(job.time, str):
            if job.time.isnumeric():
                job.time = timedelta(seconds=int(job.time))

        schedule = RQClient()
        job = schedule.schedule(job.name,
                                job.description,
                                job.time,
                                schedule_track, job.tracker_payload.dict(exclude={"metadata": ..., "operation": ...}),
                                get_ip_address(request))  # type: rq.job.Job
        return {
            "id": job.id,
            "description": job.description,
            "origin": job.origin
        }

    except UnauthorizedException as e:
        message = str(e)
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_401_UNAUTHORIZED)
    except FieldTypeConflictException as e:
        message = "FieldTypeConflictException: {} - {}".format(str(e), e.explain())
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except EventValidationException as e:
        message = "Validation failed with error: {}".format(str(e))
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except TracardiException as e:
        message = str(e)
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
