from json import JSONDecodeError
from fastapi import APIRouter, Request, HTTPException, Depends

from app.api.auth.authentication import get_current_user
from app.setup.on_start import update_api_instance

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/healthcheck", tags=["health"])
async def track(r: Request):
    try:
        print(r.headers)
        # from time import sleep
        # sleep(5)
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.get("/healthcheck", tags=["health"])
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.put("/healthcheck", tags=["health"])
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.delete("/healthcheck", tags=["health"])
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.get("/health/report/instance", tags=["health"])
async def register_api_instance_health():
    try:
        return await update_api_instance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
