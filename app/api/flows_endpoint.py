from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from .auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.mysql.interface import workflow_dao

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/flows/entity", tags=["flow"],
            include_in_schema=tracardi.expose_gui_api)
async def get_flows_entities(type: Optional[str] = None, limit: int = 500):
    """
    Loads flows according to given limit (int) parameter
    """
    result, total = await workflow_dao.load_named_entities(limit)
    return {
        "total": total,
        "result": result
    }


@router.get("/flows", tags=["flow"], include_in_schema=tracardi.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
@router.get("/flows/by_tag", tags=["flow"], include_in_schema=tracardi.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
async def get_flows(type: Optional[str] = None, query: str = None, limit: int = 100):
    """
    Returns workflows grouped according to given query (str) and limit (int) parameters
    """
    result, total = await workflow_dao.load_flows(type, limit, search=query)

    return {
        "total": total,
        "grouped": {
            "Workflows": result
        }
    }
