from collections import defaultdict
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends

from tracardi.service.storage.driver import storage
from app.service.grouper import search
from tracardi.domain.segment import Segment
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


async def _load_record(id: str) -> Optional[Segment]:
    return Segment.create(await storage.driver.segment.load_by_id(id))


@router.get("/segment/{id}",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segment(id: str):
    """
    Returns segment with given ID (str)
    """
    return await _load_record(id)


@router.delete("/segment/{id}",
               tags=["segment"],
               include_in_schema=server.expose_gui_api)
async def delete_segment(id: str):
    """
    Deletes segment with given ID (str)
    """

    result = await storage.driver.segment.delete_by_id(id)

    await storage.driver.segment.refresh()
    return result


@router.get("/segments/refresh",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def refresh_segments():
    """
    Refreshes segments index
    """
    return await storage.driver.segment.refresh()


@router.get("/segments",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segments(query: str = None):
    """
    Returns segments with match of given query (str) on name of event type
    """
    result = await storage.driver.segment.load_all()
    total = result.total
    result = [Segment.construct(Segment.__fields_set__, **r) for r in result]

    # Filtering
    if query is not None and len(query) > 0:
        query = query.lower()
        if query:
            result = [r for r in result if
                      query in r.name.lower() or (r.eventType is not None and search(query, [r.eventType]))]

    # Grouping
    groups = defaultdict(list)
    for segment in result:  # type: Segment
        if isinstance(segment.eventType, list):
            if not segment.eventType:
                groups["Global"].append(segment)
            else:
                for group in segment.eventType:
                    groups[group].append(segment)
        elif isinstance(segment.eventType, str):
            groups[segment.eventType].append(segment)
        else:
            groups["Global"].append(segment)

    # Sort
    groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

    return {
        "total": total,
        "grouped": groups
    }


@router.post("/segment",
             tags=["segment"],
             response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_segment(segment: Segment):
    """
    Adds new segment to database
    """
    result = await storage.driver.segment.save(segment.dict())
    await storage.driver.segment.refresh()
    return result
