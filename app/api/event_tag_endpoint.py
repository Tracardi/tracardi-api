from tracardi.service.storage.driver import storage
from typing import List
from fastapi import APIRouter, Depends, Response, HTTPException
from app.config import server
from tracardi.domain.event_tag import EventTag
from .auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.post("/event-tag/replace", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def replace_tags(tag_form: EventTag):
    result = await storage.driver.tag.replace(
        event_type=tag_form.type,
        tags=tag_form.tags
    )
    await storage.driver.tag.refresh()
    await update_tags(tag_form.type)
    await storage.driver.tag.refresh_tags_cache_for_type(tag_form.type)

    return {"replaced": result.saved}


@router.post("/event-tag", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_tags(tag_form: EventTag):
    """
    Adds new tags for given event type
    """
    result = await storage.driver.tag.add(
        event_type=tag_form.type,
        tags=tag_form.tags
    )
    if result.errors:
        raise ValueError(result.errors)

    await storage.driver.tag.refresh()
    await update_tags(tag_form.type)
    await storage.driver.tag.refresh_tags_cache_for_type(tag_form.type)
    return {"new": result.saved, "updated": 1 - result.saved}


@router.delete("/event-tag", tags=["event"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_tags(tag_form: EventTag):
    """
    Deletes given tags from given event type
    """
    try:
        total, removed, result = await storage.driver.tag.remove(
                event_type=tag_form.type,
                tags=tag_form.tags
            )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    await storage.driver.tag.refresh()
    await storage.driver.tag.refresh_tags_cache_for_type(tag_form.type)

    return {"removed": removed, "total": total}


@router.get("/event-tag", tags=["event"], include_in_schema=server.expose_gui_api, response_model=List[dict])
async def get_tags(limit: int = 100, query: str = ""):
    """
    Loads event tags with defined limit (int)
    """
    return await storage.driver.tag.load_tags(limit=limit, query_string=query)


@router.get("/event-tags/flush", tags=["event"], include_in_schema=server.expose_gui_api)
async def flush_tags_index():
    """
    Flushes tags index
    """
    return await storage.driver.tag.flush()


@router.get("/event-tags/refresh", tags=["event"], include_in_schema=server.expose_gui_api)
async def refresh_tags_index():
    """
    Refreshes tags index
    """
    return await storage.driver.tag.refresh()


@router.put("/event-tag/type/{event_type}", tags=["event"],
            include_in_schema=server.expose_gui_api, response_model=dict)
async def update_tags(event_type: str):
    """
    Updates tags in all events of given event type (str)
    """
    search_result = await storage.driver.tag.get_by_type(event_type)
    record = list(search_result).pop() if search_result else {}
    tags = EventTag(**record).tags
    update_result = await storage.driver.event.update_tags(event_type=event_type, tags=tags)
    return {
        "total": update_result["updated"]
    }


@router.delete("/event-tag/{event_type}", tags=["event"],
               include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_record(event_type: str, response: Response):
    """
    Deletes all information about tags for given event type (str)
    """

    delete_result = await storage.driver.tag.delete(event_type)
    await storage.driver.tag.refresh()
    await storage.driver.tag.refresh_tags_cache_for_type(event_type)
    if delete_result is None:
        response.status_code = 404
    return {"deleted": 0 if delete_result is None else 1}
