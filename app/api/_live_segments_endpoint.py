# from datetime import datetime
# from typing import Optional
#
# from fastapi import APIRouter, HTTPException
# from fastapi import Depends
#
# from tracardi.domain.live_segment import WorkflowSegmentationTrigger
# from tracardi.service.storage.mysql.mapping.segment_trigger_mapping import map_to_workflow_segmentation_trigger
# from tracardi.service.storage.mysql.service.workflow_segmentation_trigger_service import \
#     WorkflowSegmentationTriggerService
# from .auth.permissions import Permissions
# from tracardi.config import tracardi
# from ..service.grouping import get_grouped_result
# from tracardi.service.utils.date import now_in_utc
#
# router = APIRouter(
#     dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
# )
#
#
# wsts = WorkflowSegmentationTriggerService()
#
# @router.get("/segment/live/{id}",
#             tags=["segment"],
#             include_in_schema=tracardi.expose_gui_api)
# async def get_live_segment(id: str) -> Optional[WorkflowSegmentationTrigger]:
#     """
#     Returns live segment with given ID (str)
#     """
#
#     record = await wsts.load_by_id(id)
#
#     if not record.exists():
#         raise HTTPException(status_code=404, detail=f"Workflow segmentation trigger id={id} does not exist.")
#
#     return record.map_to_object(map_to_workflow_segmentation_trigger)
#
#
# @router.delete("/segment/live/{id}",
#                tags=["segment"],
#                include_in_schema=tracardi.expose_gui_api)
# async def delete_live_segment(id: str):
#     """
#     Deletes live segment with given ID (str)
#     """
#
#     return await wsts.delete_by_id(id)
#
#
# @router.get("/segments/live",
#             tags=["segment"],
#             include_in_schema=tracardi.expose_gui_api)
# async def get_workflow_segmentation_triggers(query: str = None, limit: int = 100):
#     """
#     Returns workflow segmentation triggers with match of given query (str) on name of event type
#     """
#
#     records = await wsts.load_all(search=query, limit=100)
#     return get_grouped_result("Workflow segmentations", records, map_to_workflow_segmentation_trigger)
#
#
# @router.post("/segment/live",
#              tags=["segment"],
#              include_in_schema=tracardi.expose_gui_api)
# async def upsert_live_segment(segment: WorkflowSegmentationTrigger):
#     """
#     Adds new live segment to database
#     """
#
#     segment.timestamp = now_in_utc()
#     return await wsts.insert(segment)
