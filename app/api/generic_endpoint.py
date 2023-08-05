from typing import Optional

from fastapi import APIRouter
from fastapi import Depends

from tracardi.config import tracardi
from tracardi.service.kql.autocomplete import KQLAutocomplete
from tracardi.service.storage.driver.elastic import raw as raw_db
from tracardi.domain.enum.indexes_histogram import IndexesHistogram
from tracardi.domain.enum.indexes_search import IndexesSearch
from tracardi.domain.sql_query import SqlQuery
from tracardi.domain.time_range_query import DatetimeRangePayload
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer", "maintainer"]))]
)


@router.get("/{index}/query/autocomplete",
            tags=["autocomplete"],
            include_in_schema=server.expose_gui_api)
async def autocomplete_kql(index: IndexesSearch, query: Optional[str] = ""):
    try:
        ac = KQLAutocomplete(index=index.value)
        next_values, current = await ac.autocomplete(query)
        return {
            "next": next_values,
            "current": current
        }
    except Exception as e:
        print(e)
        return []


@router.post("/{index}/select",
             tags=["data"],
             include_in_schema=server.expose_gui_api)
async def select_by_sql(index: IndexesSearch, query: Optional[SqlQuery] = None):
    if query is None:
        query = SqlQuery()
    result = await raw_db.index(index.value).query_by_sql(query.where, start=0, limit=query.limit)
    return result.dict()


@router.post("/{index}/select/range/page/{page}",
             tags=["data"],
             include_in_schema=server.expose_gui_api)
@router.post("/{index}/select/range",
             tags=["data"],
             include_in_schema=server.expose_gui_api)
async def time_range_with_sql(index: IndexesHistogram, query: DatetimeRangePayload, page: Optional[int] = None,
                              query_type: str = None):
    if query_type is None:
        query_type = tracardi.query_language

    if page is not None:
        page_size = 25
        query.start = page_size * page
        query.limit = page_size
    return await raw_db.index(index.value).query_by_sql_in_time_range(query, query_type)


@router.post("/{index}/select/histogram",
             tags=["data"],
             include_in_schema=server.expose_gui_api)
async def histogram_with_sql(index: IndexesHistogram, query: DatetimeRangePayload, query_type: str = None,
                             group_by: str = None):
    if query_type is None:
        query_type = tracardi.query_language

    return await raw_db.index(index.value).histogram_by_sql_in_time_range(query, query_type, group_by)
