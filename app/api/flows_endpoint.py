from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from tracardi.service.storage.driver.elastic import flow as flow_db
from tracardi.service.wf.domain.named_entity import NamedEntity
from app.service.grouper import search
from tracardi.domain.flow import FlowRecord
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/flows/entity", tags=["flow"],
            include_in_schema=server.expose_gui_api)
async def get_flows_entities(type: Optional[str] = None, limit: int = 500):
    """
    Loads flows according to given limit (int) parameter
    """

    if type is None:
        result = await flow_db.load_all(limit=limit)
    else:
        result = await flow_db.filter(type=type, limit=limit)

    total = result.total
    result = [NamedEntity(**r) for r in result]

    return {
        "total": total,
        "result": result,
    }


@router.get("/flows", tags=["flow"],
            include_in_schema=server.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
async def get_flows(query: str = None):
    """
    Gets flows that match given query (str) with their name
    """
    result = await flow_db.load_all(limit=200)
    total = result.total
    result = [FlowRecord(**r) for r in result]

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if query in r.name.lower() or search(query, r.projects)]

    return {
        "total": total,
        "result": result,
    }


@router.get("/flows/refresh", tags=["flow"], include_in_schema=server.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
async def refresh_flows():
    """
    Refreshed flow index
    """
    return await flow_db.refresh()


@router.get("/flows/by_tag", tags=["flow"], include_in_schema=server.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
async def get_grouped_flows(type: Optional[str] = None, query: str = None, limit: int = 100):
    """
    Returns workflows grouped according to given query (str) and limit (int) parameters
    """
    if type is None:
        result = await flow_db.load_all(limit=limit)
    else:
        result = await flow_db.filter(type=type, limit=limit)
    return group_records(result, query, group_by='projects', search_by='name', sort_by='name')
