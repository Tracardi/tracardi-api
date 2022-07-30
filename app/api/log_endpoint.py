from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.service.storage.driver import storage

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/logs/page/{page}", tags=["logs"], include_in_schema=server.expose_gui_api)
@router.get("/logs", tags=["logs"], include_in_schema=server.expose_gui_api)
async def get_logs(page: Optional[int] = None, query: Optional[str] = None):
    """
    Returns list of all Tracardi API logs. Accessible by roles: "admin"
    """
    try:
        if page is None:
            page = 0
            page_size = 100
        else:
            page_size = server.page_size * 2
        start = page * page_size
        limit = page_size

        result = await storage.driver.log.load_all(start, limit) if query is None else \
            await storage.driver.log.load_by_query_string(query, start, limit)

        return {
            "total": result.total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

