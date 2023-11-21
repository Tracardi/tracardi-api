from typing import List, Optional

from fastapi import APIRouter, Response, HTTPException, Depends

from tracardi.domain.event_source import EventSource
from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.service.storage.driver.elastic import rule as rule_db
from tracardi.service.storage.driver.elastic import flow as flow_db
from tracardi.domain.rule import Rule
from tracardi.service.storage.mysql.mapping.event_source_mapping import map_to_event_source
from tracardi.service.storage.mysql.service.event_source_service import EventSourceService
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.post("/rule", tags=["rule"], include_in_schema=tracardi.expose_gui_api)
async def upsert_rule(rule: Rule):
    """
    Adds new trigger rule to database
    """

    if rule.type == 'event-collect':
        event_source: Optional[EventSource] = (await EventSourceService().load_by_id(rule.source.id)).map_to_object(map_to_event_source)
        # event_source = await event_source_db.load(rule.source.id)

        if event_source is None:
            raise HTTPException(status_code=422, detail='Incorrect source id: `{}`'.format(rule.source.id))

    if not rule.name:
        if rule.type == 'segment-add':
            rule.name = f"Trigger \"{rule.flow.name}\" with segment \"{rule.segment.name}\""
        elif rule.type == 'event-collect':
            rule.name = f"Trigger \"{rule.flow.name}\" with event \"{rule.event_type.name}\""

    if not rule.description:
        if rule.type == 'segment-add':
            rule.description = f"Triggers workflow: \"{rule.flow.name}\" when segment \"{rule.segment.name}\" " \
                               f"is added to profile."
        elif rule.type == 'event-collect':
            rule.description = f"Triggers workflow: \"{rule.flow.name}\" when event \"{rule.event_type.name}\" " \
                               f"is collected from source: \"{rule.source.name}\""

    flow_record = await flow_db.load_record(rule.flow.id)
    if flow_record is None:
        new_flow = FlowMetaData(id=rule.flow.id, name=rule.flow.name, description="", type='collection')
        await flow_db.save(new_flow)

    result = await rule_db.save(rule)

    await rule_db.refresh()

    return result


@router.get("/rule/{id}", tags=["rule"], response_model=Optional[Rule], include_in_schema=tracardi.expose_gui_api)
async def get_rule(id: str, response: Response):
    """
    Returns rule or None if rule does not exist.
    """

    result = await rule_db.load_by_id(id)

    if result is None:
        response.status_code = 404
        return None

    return result


@router.delete("/rule/{id}", tags=["rule"], include_in_schema=tracardi.expose_gui_api)
async def delete_rule(id: str, response: Response):
    """
    Deletes rule with given ID (str) from database
    """
    result = await rule_db.delete_by_id(id)

    if result is None:
        response.status_code = 404
        return None

    await rule_db.refresh()
    return result


@router.get("/rules/by_flow/{id}", tags=["rules"], response_model=List[Rule], include_in_schema=tracardi.expose_gui_api)
async def get_rules_attached_to_flow(id: str) -> List[Rule]:
    """
    Returns list of rules attached to flow with given ID (str)
    """
    return await rule_db.load_flow_rules(id)


@router.get("/rules/refresh", tags=["rules"], include_in_schema=tracardi.expose_gui_api)
async def refresh_rules():
    """
    Refreshes rules index
    """
    return await rule_db.refresh()


@router.get("/rules/flash", tags=["rules"], include_in_schema=tracardi.expose_gui_api)
async def flash_rules():
    """
    Flushes rules index
    """
    return await rule_db.flush()


@router.get("/rules/by_tag", tags=["rules"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_rules_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    """
    Lists rules by tags, according to query (str), start (int) and limit (int) parameters
    """
    result = await rule_db.load_all(start, limit=limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')


@router.get("/rules/by_event_type/{event_type}", tags=["rules"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_rules_by_event_type(event_type: str) -> dict:
    """
    Lists rules by event types
    """
    result = await rule_db.load_by_event_type(event_type)
    return result.dict()
