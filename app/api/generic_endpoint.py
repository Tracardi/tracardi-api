from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.config import tracardi
from tracardi.service.storage.driver import storage
from tracardi.domain.enum.indexes_histogram import IndexesHistogram
from tracardi.domain.enum.indexes_search import IndexesSearch
from tracardi.domain.sql_query import SqlQuery
from tracardi.domain.time_range_query import DatetimeRangePayload
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.post("/{index}/select",
             tags=["generic", "event", "profile", "resource", "rule", "session", "flow", "segment"],
             include_in_schema=server.expose_gui_api)
async def select_by_sql(index: IndexesSearch, query: Optional[SqlQuery] = None):
    try:
        if query is None:
            query = SqlQuery()
        return await storage.driver.raw.index(index.value).query_by_sql(query.where, start=0, limit=query.limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{index}/select/range/page/{page}",
             tags=["generic", "event", "profile", "resource", "rule", "session", "flow", "segment"],
             include_in_schema=server.expose_gui_api)
@router.post("/{index}/select/range",
             tags=["generic", "event", "profile", "resource", "rule", "session", "flow", "segment"],
             include_in_schema=server.expose_gui_api)
async def time_range_with_sql(index: IndexesHistogram, query: DatetimeRangePayload, page: Optional[int] = None,
                              query_type: str = None):
    try:

        if query_type is None:
            query_type = tracardi.query_language

        if page is not None:
            page_size = 25
            query.start = page_size * page
            query.limit = page_size
        return await storage.driver.raw.index(index.value).query_by_sql_in_time_range(query, query_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{index}/select/histogram",
             tags=["generic", "event", "profile", "resource", "rule", "session", "flow", "segment"],
             include_in_schema=server.expose_gui_api)
async def histogram_with_sql(index: IndexesHistogram, query: DatetimeRangePayload, query_type: str = None):
    try:

        if query_type is None:
            query_type = tracardi.query_language

        return await storage.driver.raw.index(index.value).histogram_by_sql_in_time_range(query, query_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
