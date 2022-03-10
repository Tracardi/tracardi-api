from fastapi import APIRouter, Depends, HTTPException
from .auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from elasticsearch import ElasticsearchException


class LogPayload(BaseModel):
    email: str
    successful: bool


router = APIRouter(
    dependencies=[
        Depends(get_current_user)
    ]
)


@router.get("/user-logs", tags=["user-logs"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_user_logs(start: int = 0, limit: int = 100):
    """
    Returns all user logs
    """
    try:
        result = await storage.driver.user_log.load_logs(start, limit)
        return list(result)

    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-logs/{lower}/{upper}", tags=["user-logs"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_logs_within_period(lower: int, upper: int, start: int = 0, limit: int = 100):
    """
    Returns user logs within given time period
    """
    try:
        result = await storage.driver.user_log.load_within_period(
            upper,
            lower,
            start=start,
            limit=limit
        )
        return [hit["_source"] for hit in result["hits"]["hits"]]

    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user-logs/by-email/{email}", tags=["user-logs"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def get_logs_for_user(email: str, start: int = 0, limit: int = 100):
    """
    Returns user logs within given time period
    """
    try:
        result = await storage.driver.user_log.load_by_user(
            email=email,
            start=start,
            limit=limit
        )
        return [hit["_source"] for hit in result["hits"]["hits"]]

    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))

