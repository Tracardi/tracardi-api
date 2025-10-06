import email

from time import time
from json import JSONDecodeError
from typing import Optional

from fastapi import APIRouter, Request, status, HTTPException, Response
from fastapi.responses import RedirectResponse

from tracardi.context import get_context
from tracardi.domain.event_redirect import EventRedirect
from tracardi.service.ip_address import get_ip_address
from tracardi.service.notation.dict_traverser import DictTraverser
from tracardi.service.notation.dot_accessor import DotAccessor

from app.api.track.service.http import get_headers
from tracardi.domain.entity import Entity, PrimaryEntity
from tracardi.domain.event_metadata import EventPayloadMetadata
from tracardi.domain.payload.event_payload import EventPayload
from tracardi.domain.time import Time
from tracardi.service.storage.mysql.mapping.event_redirect_mapping import map_to_event_redirect
from tracardi.service.storage.mysql.service.event_redirect_service import EventRedirectService
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.exceptions.exception import UnauthorizedException, FieldTypeConflictException, \
    EventValidationException, BlockedException, InvalidBotTrafficException
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.track_event import track_event
from tracardi.service.url_constructor import url_query_params_to_dict
from tracardi.service.utils.hasher import hash_id

logger = get_logger(__name__)

router = APIRouter()


async def parse_properties(request: Request):
    if request.headers.get('Content-Type', '').lower().startswith('application/json'):
        try:
            return await request.json()
        except JSONDecodeError:
            raise ValueError(f"Could not parse body content to JSON. Body content {await request.body()}")
    elif request.headers.get('Content-Type', '').lower() in ['multipart/form-data',
                                                             'application/x-www-form-urlencoded']:
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
    except InvalidBotTrafficException as e:
        message = str(e)
        logger.info(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except BlockedException as e:
        message = str(e)
        logger.warning(message)
        raise HTTPException(detail=message,
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)
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
        message = str(e)

        logger.error(f"Validation error when processing {tracker_payload}. Details: {message}")
        raise HTTPException(detail=message,
                            status_code=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        message = str(e)

        logger.error(f"Error when processing {tracker_payload}. Details: {message}")
        raise HTTPException(detail=message,
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        pass


@router.post("/track", tags=['collector'])
async def track(tracker_payload: TrackerPayload, request: Request, response: Response, profile_less: bool = False):
    start = time()

    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = profile_less
    result = await _track(tracker_payload,
                          get_ip_address(request),
                          allowed_bridges=['rest'])

    if isinstance(result, dict) and result.get('errors', []):
        response.status_code = 226

    passed_time = time() - start
    logger.info(f"Regular: Track finished in {passed_time}s")

    # if passed_time> 5:
    #     print(get_context().profiler.report())

    return result


@router.patch("/track", tags=['collector'])
async def track(tracker_payload: TrackerPayload, request: Request, response: Response, profile_less: bool = False):
    start = time()

    tracker_payload.options['queue'] = True
    tracker_payload.set_headers(dict(request.headers))
    tracker_payload.profile_less = profile_less
    result = await _track(tracker_payload,
                          get_ip_address(request),
                          allowed_bridges=['rest'])

    if result and result.get('errors', []):
        response.status_code = 226

    passed_time = time() - start
    logger.info(f"Queue: Track finished in {passed_time}s")
    # if passed_time> 5:
    #     print(get_context().profiler.report())

    return result


@router.post("/collect/{event_type}/{source_id}/{session_id}", tags=['collector'])
@router.post("/collect/{event_type}/{source_id}/{session_id}/", tags=['collector'])
async def track_post_webhook_with_session(event_type: str, source_id: str, request: Request,
                                          session_id: Optional[str] = None):
    """
    Collects data from request POST and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """

    properties = await parse_properties(request)

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
@router.get("/collect/{event_type}/{source_id}/{session_id}/", tags=['collector'])
async def track_get_webhook(event_type: str, source_id: str, request: Request, session_id: Optional[str] = None):
    """
    Collects data from request GET and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """

    properties = url_query_params_to_dict(request.url.query)

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
@router.get("/collect/{event_type}/{source_id}/", tags=['collector'])
async def track_get_webhook(event_type: str, source_id: str, request: Request):
    """
    Collects data from request GET and adds event type. It stays profile-less if no session provided.
    Session is saved when event is not profile less.
    """

    properties = url_query_params_to_dict(request.url.query)

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
@router.post("/collect/{event_type}/{source_id}/", tags=['collector'])
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


@router.get("/redirect/{redirect_id}/s/{session_id}", tags=["collector"])
@router.get("/redirect/{redirect_id}", tags=["collector"])
@router.get("/redirect/{redirect_id}/p/{profile_id}", tags=["collector"])
@router.get("/redirect/{redirect_id}/pii/{hash_type}/{pii_data}", tags=["collector"])
async def request_redirect(request: Request, redirect_id: str,
                           session_id: Optional[str] = None,
                           profile_id: Optional[str] = None,
                           hash_type: Optional[str] = None,
                           pii_data: Optional[str] = None,
                           ):
    """
       Redirects events
    """

    if profile_id:
        profile_id = profile_id.strip()

    if session_id:
        session_id = session_id.strip()

    hashed_id = None
    if hash_type and pii_data and hash_type in ['emm', 'phm']:
        profile_id = hash_id(pii_data, hash_type)
        hashed_id = [profile_id]

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

    dot = DotAccessor(
        payload={
            "params": dict(request.query_params),
            "body": body
        },
    )
    converter = DictTraverser(dot)

    event_redirect: EventRedirect = redirect_record.map_to_object(map_to_event_redirect)

    properties = converter.reshape(event_redirect.props)
    tracker_payload = TrackerPayload(
        source=Entity(id=event_redirect.source.id),
        session=Entity(id=session_id) if session_id else None,
        profile=PrimaryEntity(id=profile_id, ids=hashed_id) if profile_id else None,
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
    tracker_payload.profile_less = not session_id and not profile_id
    await _track(
        tracker_payload,
        get_ip_address(request),
        allowed_bridges=['redirect']
    )

    return RedirectResponse(event_redirect.url)
