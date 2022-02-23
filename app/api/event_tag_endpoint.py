from tracardi.service.storage.driver import storage
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from .auth.authentication import get_current_user
from tracardi.domain.event_tag import EventTag
from tracardi.exceptions.exception import StorageException

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/event/tag/add", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_tags(tag_form: EventTag):
    """
    Adds new tags for given event type
    """
    result = await storage.driver.tag.add(
        event_type=tag_form.type,
        tags=tag_form.tags
    )
    if result.errors:
        raise HTTPException(status_code=500, detail=result.errors)
    return {"new": result.saved, "updated": 1 - result.saved}


@router.delete("/event/tag/delete", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_tags(tag_form: EventTag):
    """
    Deletes given tags from given event type
    """
    try:
        total, removed, result = await storage.driver.tag.remove(
            event_type=tag_form.type,
            tags=tag_form.tags
        )
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"removed": removed, "total": total}


@router.get("/event/tag/get", tags=["event"], include_in_schema=server.expose_gui_api, response_model=List[dict])
async def get_tags(limit: int = 100):
    """
    Loads event tags with defined limit (int)
    """
    return (await storage.driver.tag.load_tags(limit=limit)).dict()["result"]


@router.put("/event/tag/type/{event_type}", tags=["event"],
            include_in_schema=server.expose_gui_api, response_model=dict)
async def update_tags(event_type: str):
    """
    Updates tags in all events of given event type (str)
    """
    try:
        search_result = await storage.driver.tag.get_by_type(event_type)
        record = list(search_result).pop() if search_result else {}
        tags = EventTag(**record).tags
        update_result = await storage.driver.event.update_tags(event_type=event_type, tags=tags)
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "total": update_result["updated"]
    }


@router.delete("/event/tag/delete/{event_type}", tags=["event"],
               include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_record(event_type: str):
    """
    Deletes all information about tags for given event type (str)
    """
    try:
        delete_result = await storage.driver.tag.delete(event_type)
    except StorageException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 0 if delete_result is None else 1}
