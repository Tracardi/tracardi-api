import logging
from fastapi import APIRouter, Request
from fastapi import HTTPException
from tracardi.domain.api_instance import ApiInstance

from app.api.track.service.synchronizer import ProfileTracksSynchronizer
from app.api.track.service.tracker import track_event
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException, UnauthorizedException, FieldTypeConflictException

logger = logging.getLogger('tracardi.api.event_server')
logger.setLevel(logging.WARNING)

router = APIRouter()


@router.post("/track", tags=['tracker'])
async def track(tracker_payload: TrackerPayload, request: Request):
    try:
        if tracardi.sync_profile_tracks:
            async with ProfileTracksSynchronizer(tracker_payload.profile, wait=1):
                return await track_event(tracker_payload, ip=request.client.host)
        else:
            return await track_event(tracker_payload, ip=request.client.host)
    except UnauthorizedException as e:
        logger.error(str(e))
        raise HTTPException(detail=str(e), status_code=401)
    except FieldTypeConflictException as e:
        logger.error(str(e))
        raise HTTPException(detail="{} - {}".format(str(e), e.explain()), status_code=422)
    except TracardiException as e:
        logger.error(str(e))
        raise HTTPException(detail=str(e), status_code=500)
    finally:
        api_instance = ApiInstance()
        api_instance.increase_track_requests()
