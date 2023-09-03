from collections import defaultdict
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends

from tracardi.domain.named_entity import NamedEntity
from tracardi.service.storage.driver.elastic import segment as segment_db
from app.service.grouper import search
from tracardi.domain.segment import Segment
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


async def _load_record(id: str) -> Optional[Segment]:
    return Segment.create(await segment_db.load_by_id(id))


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

    result = await segment_db.delete_by_id(id)

    await segment_db.refresh()
    return result


@router.get("/segments/refresh",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def refresh_segments():
    """
    Refreshes segments index
    """
    return await segment_db.refresh()


@router.get("/segments",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segments(query: str = None):
    """
    Returns segments with match of given query (str) on name of event type
    """
    result = await segment_db.load_all()
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


@router.get("/segments/metadata",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segments_metadata(name: str = ""):
    """
    Returns segments with match of given query (str) on name of event type
    """
    result = await segment_db.load_by_name(name)
    total = result.total
    result = [NamedEntity(**r) for r in result]

    return {
        "total": total,
        "grouped": result
    }


@router.post("/segment",
             tags=["segment"],
             response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_segment(segment: Segment):
    """
    Adds new segment to database
    """
    result = await segment_db.save(segment.model_dump())
    await segment_db.refresh()
    return result
