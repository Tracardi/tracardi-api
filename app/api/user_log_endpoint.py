from fastapi import APIRouter, Depends
from tracardi.config import tracardi
from tracardi.service.storage.driver.elastic import user_log as user_log_db
from pydantic import BaseModel
from typing import Optional
from .auth.permissions import Permissions
from ..config import server


class LogPayload(BaseModel):
    email: str
    successful: bool


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/user-logs/page/{page}", tags=["user-logs"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_user_logs(page: Optional[int] = None, query: Optional[str] = None):
    """
    Returns user logs according to given parameters
    """
    if page is None:
        page = 0
        page_size = 50
    else:
        page_size = server.page_size * 2
    start = page * page_size
    limit = page_size
    # todo ERROR this does not exist
    result = await user_log_db.load_logs(start, limit, query)
    return {
        "total": result.total,
        "result": list(result)
    }
