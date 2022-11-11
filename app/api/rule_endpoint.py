import asyncio
from typing import List, Optional

from fastapi import APIRouter, Response, HTTPException, Depends

from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.service.storage.driver import storage
from tracardi.domain.rule import Rule
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/rule/{id}", tags=["rule"], response_model=Optional[Rule], include_in_schema=server.expose_gui_api)
async def get_rule(id: str, response: Response):
    """
    Returns rule or None if rule does not exist.
    """

    result = await storage.driver.rule.load_by_id(id)

    if result is None:
        response.status_code = 404
        return None

    return result


@router.post("/rule", tags=["rule"], include_in_schema=server.expose_gui_api)
async def upsert_rule(rule: Rule):
    """
    Adds new rule to database
    """
    # Check if source id exists
    event_source = await storage.driver.event_source.load(rule.source.id)

    if event_source is None:
        raise HTTPException(status_code=422, detail='Incorrect source id: `{}`'.format(rule.source.id))

    flow_record = await storage.driver.flow.load_record(rule.flow.id)
    add_flow_task = None
    if flow_record is None:
        new_flow = FlowMetaData(id=rule.flow.id, name=rule.flow.name, description="", type='collection')
        add_flow_task = asyncio.create_task(storage.driver.flow.save(new_flow))

    add_rule_task = asyncio.create_task(storage.driver.rule.save(rule))

    if add_flow_task:
        await add_flow_task

    result = await add_rule_task

    await storage.driver.rule.refresh()

    return result


@router.delete("/rule/{id}", tags=["rule"], include_in_schema=server.expose_gui_api)
async def delete_rule(id: str, response: Response):
    """
    Deletes rule with given ID (str) from database
    """
    result = await storage.driver.rule.delete_by_id(id)

    if result is None:
        response.status_code = 404
        return None

    await storage.driver.rule.refresh()
    return result


@router.get("/rules/by_flow/{id}", tags=["rules"], response_model=List[Rule], include_in_schema=server.expose_gui_api)
async def get_rules_attached_to_flow(id: str) -> List[Rule]:
    """
    Returns list of rules attached to flow with given ID (str)
    """
    return await storage.driver.rule.load_flow_rules(id)


@router.get("/rules/refresh", tags=["rules"], include_in_schema=server.expose_gui_api)
async def refresh_rules():
    """
    Refreshes rules index
    """
    return await storage.driver.rule.refresh()


@router.get("/rules/flash", tags=["rules"], include_in_schema=server.expose_gui_api)
async def refresh_rules():
    """
    Flushes rules index
    """
    return await storage.driver.rule.flush()


@router.get("/rules/by_tag", tags=["rules"], response_model=dict, include_in_schema=server.expose_gui_api)
async def get_rules_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    """
    Lists rules by tags, according to query (str), start (int) and limit (int) parameters
    """
    result = await storage.driver.rule.load_all(start, limit=limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
