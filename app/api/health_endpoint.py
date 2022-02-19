from json import JSONDecodeError
from fastapi import APIRouter, Request, HTTPException, Depends

from app.api.auth.authentication import get_current_user
from app.config import server
from app.setup.on_start import update_api_instance

router = APIRouter(
    # dependencies=[Depends(get_current_user)]
)


@router.post("/healthcheck", tags=["health"], include_in_schema=server.expose_gui_api)
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
    except JSONDecodeError as e:
        return await r.body()


@router.get("/healthcheck", tags=["health"], include_in_schema=server.expose_gui_api)
async def get_healthcheck(r: Request):
    """
       Enables you to see if API responds to HTTP GET requests
    """
    try:
        return {
            "headers": r.headers,
            "json": await r.json(),
            "body": await r.body()
        }
    except JSONDecodeError as e:
        return await r.body()


@router.put("/healthcheck", tags=["health"], include_in_schema=server.expose_gui_api)
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
    except JSONDecodeError as e:
        return await r.body()


@router.delete("/healthcheck", tags=["health"], include_in_schema=server.expose_gui_api)
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
    except JSONDecodeError as e:
        return await r.body()


@router.get("/health/report/instance", tags=["health"], include_in_schema=server.expose_gui_api)
async def register_api_instance_health():
    """
    Returns the health check of a running instance
    """
    try:
        return await update_api_instance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
