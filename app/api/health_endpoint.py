from json import JSONDecodeError
from fastapi import APIRouter, Request, HTTPException
from tracardi.config import tracardi

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


