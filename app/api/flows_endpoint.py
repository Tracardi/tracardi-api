from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from tracardi.service.storage.mysql.map_to_named_entity import map_to_named_entity
from tracardi.service.storage.mysql.mapping.workflow_mapping import map_to_workflow_record, map_to_workflow_record_meta
from tracardi.service.storage.mysql.service.workflow_service import WorkflowService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import get_grouped_result, get_result_dict

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/flows/entity", tags=["flow"],
            include_in_schema=tracardi.expose_gui_api)
async def get_flows_entities(type: Optional[str] = None, limit: int = 500):
    """
    Loads flows according to given limit (int) parameter
    """

    ws = WorkflowService()
    if type is None:
        records = await ws.load_all(
            # columns=[WorkflowTable.id, WorkflowTable.name],
            limit=limit)
    else:
        records = await ws.load_all_by_type(
            wf_type=type,
            # columns=[WorkflowTable.id, WorkflowTable.name],
            limit=limit)

    return get_result_dict(records, map_to_named_entity)


# @router.get("/flows", tags=["flow"],
#             include_in_schema=tracardi.expose_gui_api,
#             dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
#             )
# async def get_flows(query: str = None, limit: int = 200):
#     """
#     Gets flows that match given query (str) with their name
#     """
#
#     ws = WorkflowService()
#     records = await ws.load_all(search=query, limit=limit)
#     return get_result_dict(records, map_to_workflow_record)


@router.get("/flows/by_tag", tags=["flow"], include_in_schema=tracardi.expose_gui_api,
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
            )
async def get_flows(type: Optional[str] = None, query: str = None, limit: int = 100):
    """
    Returns workflows grouped according to given query (str) and limit (int) parameters
    """
    ws = WorkflowService()
    if type is None:
        records = await ws.load_all(search=query, limit=limit)
    else:
        records = await ws.load_all_by_type(wf_type=type, search=query, limit=limit)

    return get_grouped_result("Workflows", records, map_to_workflow_record_meta)
