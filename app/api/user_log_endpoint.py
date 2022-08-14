from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from elasticsearch import ElasticsearchException
from typing import Optional
from tracardi.exceptions.exception import StorageException
from .auth.permissions import Permissions


class LogPayload(BaseModel):
    email: str
    successful: bool


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/user-logs/page/{page}", tags=["user-logs"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user_logs(page: Optional[int] = None, query: Optional[str] = None):
    """
    Returns user logs according to given parameters
    """
    try:
        if page is None:
            page = 0
            page_size = 50
        else:
            page_size = server.page_size * 2
        start = page * page_size
        limit = page_size
        # todo ERROR this does not exist
        result = await storage.driver.user_log.load_logs(start, limit, query)
        return {
            "total": result.total,
            "result": list(result)
        }

    except (ElasticsearchException, StorageException) as e:
        raise HTTPException(status_code=500, detail=str(e))
