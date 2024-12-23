from json import JSONDecodeError
from fastapi import APIRouter, Request, HTTPException

from app import state
from tracardi.config import tracardi

router = APIRouter()


@router.get("/ping", tags=["health"], include_in_schema=tracardi.expose_gui_api)
async def get_healthcheck():
    if state.server_ready:
        return 'pong'
    raise HTTPException(
        status_code=404, detail="Not ready."
    )


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
    if state.server_ready:
        return {
            "headers": r.headers,
        }
    raise HTTPException(
        status_code=404, detail="Not ready."
    )


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
