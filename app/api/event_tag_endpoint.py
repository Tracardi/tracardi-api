from tracardi.service.storage.driver import storage
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.authentication import get_current_user
from tracardi.domain.event_tag import EventTag

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/event/tag/add", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_tags(tag_form: EventTag):
    result = await storage.driver.tag.add(
        event_type=tag_form.type,
        tags=tag_form.tags
    )
    if result.errors:
        raise HTTPException(status_code=500, detail=result.errors)
    return {"OK": {"new": result.saved, "updated": 1-result.saved}}


@router.delete("/event/tag/delete", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_tags(tag_form: EventTag):
    total, removed, result = await storage.driver.tag.remove(
        event_type=tag_form.type,
        tags=tag_form.tags
    )
    if total == 0:
        return {"OK": {"removed": removed, "total": total}} if result["result"] == "deleted" else \
            {"ERROR": {"details": result["result"]}}
    else:
        return {"OK": {"removed": removed, "total": total}} if not result.errors else \
            {"ERROR": {"details": result.errors}}


@router.get("/event/tag/get", tags=["event"], include_in_schema=server.expose_gui_api, response_model=List[dict])
async def get_tags(limit: int = 100):
    return (await storage.driver.tag.load_tags(limit=limit)).dict()["result"]
