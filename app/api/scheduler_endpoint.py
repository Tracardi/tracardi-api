import logging
from datetime import datetime, timedelta
from typing import Union

import rq

from com_tracardi.scheduler.rq_clinet import RQClient
from fastapi import APIRouter, Depends, Request, HTTPException, status

from com_tracardi.scheduler.tracker import schedule_track
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import UnauthorizedException, FieldTypeConflictException, EventValidationException, \
    TracardiException
from tracardi.exceptions.log_handler import log_handler
from .auth.permissions import Permissions
from .track.service.ip_address import get_ip_address
from ..config import server

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/scheduler/jobs",
            tags=["scheduler"],
            include_in_schema=server.expose_gui_api)
async def get_scheduled_jobs():
    schedule = RQClient()
    return [{
        "time": scheduled_time,
        "job_id": job.id,
        "meta": job.meta
    } for job, scheduled_time in schedule.list()]


@router.post("/scheduler/job",
             tags=["scheduler"],
             include_in_schema=server.expose_gui_api)
async def schedule_job(
        name: str,
        time: Union[datetime, str],
        tracker_payload: TrackerPayload,
        request: Request):
    try:

        if isinstance(time, str):
            if time.isnumeric():
                time = timedelta(seconds=int(time))

        schedule = RQClient()
        job = schedule.schedule(name, time, schedule_track, tracker_payload.dict(),
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
