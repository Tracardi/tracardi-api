from json import JSONDecodeError
from fastapi import APIRouter, Request, HTTPException, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from tracardi.config import tracardi
from tracardi.domain.event import Event
from tracardi.service.storage.driver.elastic.event import get_last_event

router = APIRouter()
api_ready = False

@router.post("/healthcheck", tags=["health"], include_in_schema=tracardi.expose_gui_api)
async def post_healthcheck(r: Request):
    """
    Enables you to see if API responds to HTTP POST requests
    """
    try:
        return {
            "headers": r.headers,
            "json": await r.json(),
            "body": await r.body()
        }
    except JSONDecodeError:
        return await r.body()


@router.get("/healthcheck", tags=["health"], include_in_schema=tracardi.expose_gui_api)
async def get_healthcheck(r: Request):
    """
       Enables you to see if API responds to HTTP GET requests
    """
    try:
        if api_ready:
            return {
                "headers": r.headers,
                "json": await r.json(),
                "body": await r.body()
            }
        raise HTTPException(
            status_code=404, detail="Not ready."
        )
    except JSONDecodeError:
        return await r.body()


@router.put("/healthcheck", tags=["health"], include_in_schema=tracardi.expose_gui_api)
async def put_healthcheck(r: Request):
    """
       Enables you to see if API responds to HTTP PUT requests
    """
    try:
        return {
            "headers": r.headers,
            "json": await r.json(),
            "body": await r.body()
        }
    except JSONDecodeError:
        return await r.body()


@router.delete("/healthcheck", tags=["health"], include_in_schema=tracardi.expose_gui_api)
async def delete_healthcheck(r: Request):
    """
       Enables you to see if API responds to HTTP DELETE requests
    """
    try:
        return {
            "headers": r.headers,
            "json": await r.json(),
            "body": await r.body()
        }
    except JSONDecodeError:
        return await r.body()


@router.get("/healthcheck/event/ts", tags=["health"],
            include_in_schema=tracardi.expose_gui_api)
async def get_events_for_session():
    result = await get_last_event()

    if result is None:
        return []

    events = result.to_domain_objects(Event)

    return [{
            "id": event.id,
            "type": event.type,
            "time": event.metadata.time.insert
        } for event in events]


if tracardi.enable_prometheus:
    @router.get("/metrics", tags=['monitoring'])
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)