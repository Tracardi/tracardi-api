# from typing import Optional
#
# from fastapi import APIRouter, HTTPException
# from fastapi import Depends
#
# from tracardi.domain.segment import Segment
# from tracardi.service.storage.mysql.map_to_named_entity import map_to_named_entity
# from tracardi.service.storage.mysql.mapping.segment_mapping import map_to_segment
# from tracardi.service.storage.mysql.service.segment_service import SegmentService
# from .auth.permissions import Permissions
# from tracardi.config import tracardi
# from ..service.grouping import get_grouped_result, get_result_dict
#
# router = APIRouter(
#     dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
# )
#
#
# async def _load_record(segment_id: str) -> Optional[Segment]:
#     ss = SegmentService()
#     record = await ss.load_by_id(segment_id)
#     if not record.exists():
#         raise HTTPException(status_code=404, detail=f"No segment found for id {segment_id}")
#
#     return record.map_to_object(map_to_segment)
#
#
# @router.get("/segment/{segment_id}",
#             tags=["segment"],
#             include_in_schema=tracardi.expose_gui_api)
# async def get_segment(segment_id: str):
#     """
#     Returns segment with given ID (str)
#     """
#     return await _load_record(segment_id)
#
#
# @router.delete("/segment/{segment_id}",
#                tags=["segment"],
#                include_in_schema=tracardi.expose_gui_api)
# async def delete_segment(segment_id: str):
#     """
#     Deletes segment with given ID (str)
#     """
#     ss = SegmentService()
#     return await ss.delete_by_id(segment_id)
#
#
# @router.get("/segments",
#             tags=["segment"],
#             include_in_schema=tracardi.expose_gui_api)
# async def get_segments(query: str = None, start: int = 0, limit: int = 100):
#     """
#     Returns segments with match of given query (str) on name of event type
#     """
#
#     ss = SegmentService()
#     records = await ss.load_all(search=query, offset=start, limit=limit)
#     return get_grouped_result("Segments", records, map_to_segment)
#
#
#
# @router.post("/segment",
#              tags=["segment"],
#              include_in_schema=tracardi.expose_gui_api)
# async def upsert_segment(segment: Segment):
#     """
#     Adds new segment to database
#     """
#
#     ss = SegmentService()
#     return await ss.insert(segment)
