from collections import defaultdict
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageForBulk
from tracardi_graph_runner.domain.named_entity import NamedEntity
from .auth.authentication import get_current_user
from .grouper import search
from tracardi.domain.flow import FlowRecord
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/flows/entity", tags=["flow"], include_in_schema=server.expose_gui_api)
async def get_flows(limit: int = 500):
    try:
        result = await StorageForBulk().index('flow').load(limit=limit)
        total = result.total
        result = [NamedEntity(**r) for r in result]

        return {
            "total": total,
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows", tags=["flow"], include_in_schema=server.expose_gui_api)
async def get_flows(query: str = None):
    try:
        result = await StorageForBulk().index('flow').load()
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows/refresh", tags=["flow"], include_in_schema=server.expose_gui_api)
async def refresh_flows():
    try:
        return await storage.driver.flow.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows/by_tag", tags=["flow"], include_in_schema=server.expose_gui_api)
async def get_grouped_flows(query: str = None):
    try:
        result = await StorageForBulk().index('flow').load()
        total = result.total
        result = [FlowRecord(**r) for r in result]

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.projects)]

        # Grouping
        groups = defaultdict(list)
        for flow in result:  # type: FlowRecord
            if isinstance(flow.projects, list):
                for group in flow.projects:
                    groups[group].append(flow)
            elif isinstance(flow.projects, str):
                groups[flow.projects].append(flow)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
