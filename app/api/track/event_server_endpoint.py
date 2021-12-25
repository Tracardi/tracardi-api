import logging
from fastapi import APIRouter, Request, status, HTTPException
from tracardi.domain.api_instance import ApiInstance

from app.api.track.service.synchronizer import ProfileTracksSynchronizer
from app.api.track.service.tracker import track_event
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException, UnauthorizedException, FieldTypeConflictException, \
    EventValidationException

logger = logging.getLogger('tracardi.api.event_server')
logger.setLevel(logging.WARNING)

router = APIRouter()


@router.post("/track", tags=['tracker'])
async def track(tracker_payload: TrackerPayload, request: Request, profile_less: bool = False):
    try:
        if tracardi.sync_profile_tracks:
            async with ProfileTracksSynchronizer(tracker_payload.profile, wait=1):
                return await track_event(tracker_payload, ip=request.client.host, profile_less=profile_less)
        else:
            return await track_event(tracker_payload, ip=request.client.host, profile_less=profile_less)
    except UnauthorizedException as e:
        message = str(e)
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_401_UNAUTHORIZED)
    except FieldTypeConflictException as e:
        message = "{} - {}".format(str(e), e.explain())
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
    finally:
        api_instance = ApiInstance()
        api_instance.increase_track_requests()
