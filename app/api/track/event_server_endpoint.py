import logging
from json import JSONDecodeError

from fastapi import APIRouter, Request, status, HTTPException
from tracardi.domain.session import Session, SessionMetadata

from tracardi.domain.payload.event_payload import EventPayload

from tracardi.domain.time import Time

from tracardi.domain.api_instance import ApiInstance

from app.api.track.service.synchronizer import ProfileTracksSynchronizer
from app.api.track.service.tracker import track_event
from tracardi.config import tracardi
from tracardi.domain.event_metadata import EventPayloadMetadata
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException, UnauthorizedException, FieldTypeConflictException, \
    EventValidationException
from tracardi_graph_runner.domain.entity import Entity

logger = logging.getLogger('tracardi.api.event_server')
logger.setLevel(logging.WARNING)

router = APIRouter()


async def _track(tracker_payload: TrackerPayload, host: str, profile_less: bool = False):
    try:
        if tracardi.sync_profile_tracks:
            async with ProfileTracksSynchronizer(tracker_payload.profile, wait=1):
                return await track_event(tracker_payload, ip=host, profile_less=profile_less)
        else:
            return await track_event(tracker_payload, ip=host, profile_less=profile_less)
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


@router.post("/collect/{event_type}/{source_id}", tags=['context-server'])
async def track_webhook(event_type: str, source_id: str, request: Request):

    """
    Collects data from request POST and adds event type. Then it is sent to Tracardi as
    profile less event. Session is not saved.
    """

    try:
        properties = await request.json()
    except JSONDecodeError:
        properties = {}

    tracker_payload = TrackerPayload(
        source=Entity(id=source_id),
        session=Session(id="-1", metadata=SessionMetadata()),
        metadata=EventPayloadMetadata(time=Time()),
        profile=None,
        context={},
        properties={},
        events=[
            EventPayload(type=event_type, properties=properties)
        ],
        options={"saveSession": False}
    )
    return await _track(tracker_payload, request.client.host, profile_less=True)


@router.post("/track", tags=['context-server'])
async def track(tracker_payload: TrackerPayload, request: Request, profile_less: bool = False):
    return await _track(tracker_payload, request.client.host, profile_less)
