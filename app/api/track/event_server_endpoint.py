import logging
from json import JSONDecodeError
from typing import Optional

from fastapi import APIRouter, Request, status, HTTPException
from tracardi.domain.api_instance import ApiInstance
from tracardi.domain.entity import Entity
from tracardi.domain.event_metadata import EventPayloadMetadata
from tracardi.domain.payload.event_payload import EventPayload
from tracardi.domain.time import Time
from tracardi.service.tracker import track_event
from tracardi.config import tracardi
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import TracardiException, UnauthorizedException, FieldTypeConflictException, \
    EventValidationException
from tracardi.exceptions.log_handler import log_handler
from app.api.track.service.ip_address import get_ip_address
from tracardi.service.url_constructor import url_query_params_to_dict

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter()


async def _track(tracker_payload: TrackerPayload, host: str):
    try:
        return await track_event(
            tracker_payload,
            host,
            allowed_bridges=['rest'])
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
    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = profile_less
    return await _track(tracker_payload, get_ip_address(request))


@router.post("/collect/{event_type}/{source_id}/{session_id}", tags=['context-server'])
async def track_post_webhook(event_type: str, source_id: str, request: Request, session_id: Optional[str] = None):
    """
    Collects data from request POST and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """

    try:
        properties = await request.json()
    except JSONDecodeError:
        properties = {}

    tracker_payload = TrackerPayload(
        source=Entity(id=source_id),
        session=Entity(id=session_id),
        metadata=EventPayloadMetadata(time=Time()),
        context={},
        request={
            "headers": get_headers(request)  # it will be an event request value
        },
        properties={},
        events=[
            EventPayload(type=event_type, properties=properties)
        ],
        options={"saveSession": session_id is not None}
    )
    tracker_payload.profile_less = False
    return await _track(tracker_payload, get_ip_address(request))


@router.post("/collect/{event_type}/{source_id}", tags=['context-server'])
async def track_post_webhook(event_type: str, source_id: str, request: Request):
    """
    Collects data from request POST and adds event type. It stays profile-less.
    """

    try:
        properties = await request.json()
    except JSONDecodeError:
        properties = {}

    tracker_payload = TrackerPayload(
        source=Entity(id=source_id),
        session=None,
        metadata=EventPayloadMetadata(time=Time()),
        profile=None,
        context={},
        request={
            "headers": get_headers(request)  # it will be an event request value
        },
        properties={},
        events=[
            EventPayload(type=event_type, properties=properties)
        ],
        options={"saveSession": False}
    )
    tracker_payload.profile_less = False
    return await _track(tracker_payload, get_ip_address(request))


@router.get("/collect/{event_type}/{source_id}/{session_id}", tags=['context-server'])
async def track_get_webhook(event_type: str, source_id: str, request: Request, session_id: Optional[str] = None):
    """
    Collects data from request GET and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """
    try:
        properties = url_query_params_to_dict(request.url.query)
    except JSONDecodeError:
        properties = {}

    tracker_payload = TrackerPayload(
        source=Entity(id=source_id),
        session=Entity(id=session_id),
        metadata=EventPayloadMetadata(time=Time()),
        context={},
        request={
            "headers": get_headers(request)  # it will be an event request value
        },
        properties={},
        events=[
            EventPayload(type=event_type, properties=properties)
        ],
        options={"saveSession": session_id is not None}
    )
    tracker_payload.profile_less = False
    return await _track(tracker_payload, get_ip_address(request))


@router.get("/collect/{event_type}/{source_id}", tags=['context-server'])
async def track_get_webhook(event_type: str, source_id: str, request: Request):
    """
    Collects data from request GET and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """
    try:
        properties = url_query_params_to_dict(request.url.query)
    except JSONDecodeError:
        properties = {}

    tracker_payload = TrackerPayload(
        source=Entity(id=source_id),
        session=None,
        metadata=EventPayloadMetadata(time=Time()),
        context={},
        request={
            "headers": get_headers(request)  # it will be an event request value
        },
        properties={},
        events=[
            EventPayload(type=event_type, properties=properties)
        ],
        options={"saveSession": False}
    )
    tracker_payload.profile_less = False
    return await _track(tracker_payload, get_ip_address(request))
