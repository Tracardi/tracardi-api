import logging
from fastapi import APIRouter, Request, status, HTTPException
from app.api.track.service.ip_address import get_ip_address
from tracardi.domain.api_instance import ApiInstance
from tracardi.service.tracker import synchronized_event_tracking
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException, UnauthorizedException, FieldTypeConflictException, \
    EventValidationException
from tracardi.exceptions.log_handler import log_handler

logger = logging.getLogger('tracardi.api.event_server')
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter()


def get_headers(request: Request):
    headers = dict(request.headers)
    if 'authorization' in headers:
        del headers['authorization']
    if 'cookie' in headers:
        del headers['cookie']
    return headers


async def _track(tracker_payload: TrackerPayload, host: str, profile_less: bool = False):
    try:
        return await synchronized_event_tracking(tracker_payload, host, profile_less, allowed_bridges=['rest'])
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
    finally:
        api_instance = ApiInstance()
        api_instance.increase_track_requests()


@router.post("/track", tags=['collector'])
async def track(tracker_payload: TrackerPayload, request: Request, profile_less: bool = False):
    tracker_payload.request['headers'] = get_headers(request)
    return await _track(tracker_payload, get_ip_address(request), profile_less)
