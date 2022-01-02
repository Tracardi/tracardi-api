from collections import defaultdict
from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk

from .auth.authentication import get_current_user
from app.service.grouper import search
from tracardi.domain.entity import Entity
from tracardi.domain.segment import Segment
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/segment/{id}",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segment(id: str):
    try:
        entity = Entity(id=id)
        return await StorageFor(entity).index('segment').load(Segment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/segment/{id}",
               tags=["segment"],
               include_in_schema=server.expose_gui_api)
async def delete_segment(id: str):
    try:
        entity = Entity(id=id)
        return await StorageFor(entity).index('segment').delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/segments/refresh",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def refresh_segments():
    return await storage.driver.segment.refresh()


@router.get("/segments",
            tags=["segment"],
            include_in_schema=server.expose_gui_api)
async def get_segments(query: str = None):
    try:
        result = await StorageForBulk().index('segment').load()
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/segment",
             tags=["segment"],
             response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_source(segment: Segment):
    try:
        return await StorageFor(segment).index().save()
        # return await segment.storage().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
