from tracardi.service.storage.drivers.elastic.tag import add_tags, remove_tags, load_all_tags
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter
from app.config import server
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult


class TagForm(BaseModel):
    event_type: str = ""
    tags: List[str] = []


router = APIRouter()


@router.post("/event/tag/add", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_event_tag_endpoint(tag_form: TagForm):
    updated, result = await add_tags(
        event_type=tag_form.event_type,
        tags=tag_form.tags
    )
    return {"ERROR": {"details": result.errors}} if result.errors else {"OK": {"new": 1-updated, "updated": updated}}


@router.delete("/event/tag/delete", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_event_tag_endpoint(tag_form: TagForm):
    total, removed, result = await remove_tags(
        event_type=tag_form.event_type,
        tags=tag_form.tags
    )
    return {"ERROR": {"details": result.errors}} if isinstance(result, BulkInsertResult) and result.errors else \
        {"OK": {"removed": removed, "total": total}}


@router.get("/event/tags", tags=["event"], include_in_schema=server.expose_gui_api, response_model=List[dict])
async def get_event_tag_endpoint(limit: int = 100):
    return (await load_all_tags(limit=limit)).dict()["result"]
