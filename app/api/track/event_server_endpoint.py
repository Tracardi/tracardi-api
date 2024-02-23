from json import JSONDecodeError
from typing import Optional

from fastapi import APIRouter, Request, status, HTTPException, Response
from fastapi.responses import RedirectResponse

from tracardi.domain.event_redirect import EventRedirect
from tracardi.service.notation.dict_traverser import DictTraverser
from tracardi.service.notation.dot_accessor import DotAccessor

from app.api.track.service.http import get_headers
from tracardi.domain.entity import Entity
from tracardi.domain.event_metadata import EventPayloadMetadata
from tracardi.domain.payload.event_payload import EventPayload
from tracardi.domain.time import Time
from tracardi.service.storage.driver.elastic import session as session_db
from tracardi.service.storage.mysql.mapping.event_redirect_mapping import map_to_event_redirect
from tracardi.service.storage.mysql.service.event_redirect_service import EventRedirectService
from tracardi.service.tracker import track_event
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import UnauthorizedException, FieldTypeConflictException, \
    EventValidationException
from tracardi.exceptions.log_handler import get_logger
from app.api.track.service.ip_address import get_ip_address
from tracardi.service.url_constructor import url_query_params_to_dict

logger = get_logger(__name__)

router = APIRouter()


async def parse_properties(request: Request):
    if request.headers.get('Content-Type', '').lower().startswith('application/json'):
        try:
            return await request.json()
        except JSONDecodeError:
            return {}
    elif request.headers.get('Content-Type', '').lower() in ['multipart/form-data', 'application/x-www-form-urlencoded']:
        return await request.form()
    else:
        return await request.body()


async def _track(tracker_payload: TrackerPayload, host: str, allowed_bridges):

    if tracker_payload.source.id.startswith("@"):
        raise PermissionError("Internal event sources are not allowed via API.")

    try:
        return await track_event(
            tracker_payload,
            host,
            allowed_bridges=allowed_bridges)
    except (UnauthorizedException, PermissionError) as e:
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
    except Exception as e:
        message = str(e)
        logger.error(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/track", tags=['collector'])
async def track(tracker_payload: TrackerPayload, request: Request, response: Response, profile_less: bool = False):

    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = profile_less
    result = await _track(tracker_payload,
                        get_ip_address(request),
                        allowed_bridges=['rest'])

    if result and result.get('errors', []):
        response.status_code = 226

    return result


@router.put("/track", tags=['collector'])
async def track_async(tracker_payload: TrackerPayload, request: Request, profile_less: bool = False):

    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = profile_less

    # validate source

    # validate event and reshape event

    # queue for saving and processing


@router.post("/collect/{event_type}/{source_id}/{session_id}", tags=['collector'])
async def track_post_webhook_with_session(event_type: str, source_id: str, request: Request, session_id: Optional[str] = None):
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
    return await _track(tracker_payload,
                        get_ip_address(request),
                        allowed_bridges=['webhook'])


@router.get("/collect/{event_type}/{source_id}/{session_id}", tags=['collector'])
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
    return await _track(tracker_payload,
                        get_ip_address(request),
                        allowed_bridges=['webhook'])


@router.get("/collect/{event_type}/{source_id}", tags=['collector'])
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
    tracker_payload.profile_less = True
    return await _track(tracker_payload,
                        get_ip_address(request),
                        allowed_bridges=['webhook'])


@router.post("/collect/{event_type}/{source_id}", tags=['collector'])
async def track_post_webhook(event_type: str, source_id: str, request: Request):
    """
    Collects data from request POST and adds event type. It stays profile-less.
    """

    properties = await parse_properties(request)

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
    tracker_payload.profile_less = True
    return await _track(tracker_payload,
                        get_ip_address(request),
                        allowed_bridges=['webhook'])


@router.put("/redirect/{redirect_id}/{session_id}", tags=["collector"])
@router.delete("/redirect/{redirect_id}/{session_id}", tags=["collector"])
@router.get("/redirect/{redirect_id}/{session_id}", tags=["collector"])
@router.post("/redirect/{redirect_id}/{session_id}", tags=["collector"])
@router.put("/redirect/{redirect_id}", tags=["collector"])
@router.delete("/redirect/{redirect_id}", tags=["collector"])
@router.get("/redirect/{redirect_id}", tags=["collector"])
@router.post("/redirect/{redirect_id}", tags=["collector"])
async def request_redirect(request: Request, redirect_id: str, session_id: Optional[str] = None):
    """
       Redirects events http://localhost:8686/redirect/cce47c05-d7c3-46f8-bac9-0694d3227d9b
    """

    if session_id:
        session_id = session_id.strip()
    redirect_id = redirect_id.strip()

    ers = EventRedirectService()

    redirect_record = await ers.load_by_id(redirect_id)

    if not redirect_record.exists():
        raise HTTPException(status_code=404)

    body = {}
    if request.method in ['POST', 'PUT', 'DELETE']:
        body = await request.body()
        content_type = request.headers.get('content-type', 'xform')
        if content_type.lower().startswith('application/json'):
            try:
                body = await request.json()
            except Exception:
                body = {}

    # try to load session from cookie
    if not session_id:
        key = 'tracardi-session-id'
        if request.cookies and key in request.cookies:
            session_id = request.cookies[key]

    session = None
    if session_id:
        session = await session_db.load_by_id(session_id)

    dot = DotAccessor(
        payload={
            "params": dict(request.query_params),
            "body": body
        },
        session=session.model_dump() if session else None
    )
    converter = DictTraverser(dot)

    event_redirect: EventRedirect = redirect_record.map_to_object(map_to_event_redirect)

    properties = converter.reshape(event_redirect.props)
    tracker_payload = TrackerPayload(
        source=Entity(id=event_redirect.source.id),
        session=session,
        metadata=EventPayloadMetadata(time=Time()),
        context={},
        request={
            "headers": dict(request.headers)
        },
        properties={},
        events=[
            EventPayload(type=event_redirect.event_type, properties=properties)
        ],
        options={"saveSession": False}
    )

    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = True if not session else False
    await _track(
            tracker_payload,
            get_ip_address(request),
            allowed_bridges=['redirect']
        )

    return RedirectResponse(event_redirect.url)
