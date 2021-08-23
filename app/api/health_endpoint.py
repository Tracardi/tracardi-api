from json import JSONDecodeError
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/healthcheck")
async def track(r: Request):
    try:
        print(r.headers)
        # from time import sleep
        # sleep(5)
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.get("/healthcheck")
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.put("/healthcheck")
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()


@router.delete("/healthcheck")
async def track(r: Request):
    try:
        return await r.json()
    except JSONDecodeError as e:
        return await r.body()
