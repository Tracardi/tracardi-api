import logging
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler

from tracardi.service.storage.driver import storage

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)

# THIS is obsolete and will be removed.

@router.get("/tasks/page/{page}", tags=["tasks"], include_in_schema=server.expose_gui_api)
@router.get("/tasks", tags=["tasks"], include_in_schema=server.expose_gui_api)
async def all_tasks(page: Optional[int] = None):
    try:
        if page is None:
            page = 0
            page_size = 100
        else:
            page_size = server.page_size
        start = page * page_size
        limit = page_size
        result = await storage.driver.task.load_all(start, limit)
        return {
            "total": result.total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

