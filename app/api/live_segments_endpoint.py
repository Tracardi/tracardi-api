from collections import defaultdict
from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends

from tracardi.domain.live_segment import LiveSegment
from tracardi.service.storage.driver.elastic import live_segment as live_segment_db
from app.service.grouper import search
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/segment/live/{id}",
            tags=["segment"],
            include_in_schema=tracardi.expose_gui_api)
async def get_live_segment(id: str) -> Optional[LiveSegment]:
    """
    Returns live segment with given ID (str)
    """
    return await live_segment_db.load_by_id(id)


@router.delete("/segment/live/{id}",
               tags=["segment"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_live_segment(id: str):
    """
    Deletes live segment with given ID (str)
    """
    result = await live_segment_db.delete_by_id(id)
    await live_segment_db.refresh()
    return result


@router.get("/segments/live/refresh",
            tags=["segment"],
            include_in_schema=tracardi.expose_gui_api)
async def refresh_live_segments():
    """
    Refreshes live segments index
    """
    return await live_segment_db.refresh()


@router.get("/segments/live",
            tags=["segment"],
            include_in_schema=tracardi.expose_gui_api)
async def get_live_segments(query: str = None):
    """
    Returns live segments with match of given query (str) on name of event type
    """
    result = await live_segment_db.load_all()
    total = result.total
    result = [LiveSegment(**r) for r in result]

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if
                      query in r.name.lower() or (r.name is not None and search(query, [
                          r.name, r.description, r.workflow.name]))]

    # Grouping
    groups = defaultdict(list)
    for segment in result:  # type: LiveSegment
        groups["Live segmentation"].append(segment)

    # Sort
    groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

    return {
        "total": total,
        "grouped": groups
    }


@router.post("/segment/live",
             tags=["segment"],
             response_model=BulkInsertResult,
             include_in_schema=tracardi.expose_gui_api)
async def upsert_live_segment(segment: LiveSegment):
    """
    Adds new live segment to database
    """
    segment.timestamp = datetime.utcnow()
    result = await live_segment_db.save(segment.model_dump())
    await live_segment_db.refresh()
    return result
