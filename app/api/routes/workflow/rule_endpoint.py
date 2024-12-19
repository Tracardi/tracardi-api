from typing import List, Optional

from fastapi import APIRouter, Response, HTTPException, Depends

from tracardi.domain.event_source import EventSource
from tracardi.domain.flow import FlowRecord
from tracardi.domain.rule import Rule
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.mysql.interface import event_source_dao
from tracardi.service.storage.mysql.interface import workflow_dao
from tracardi.service.storage.mysql.interface import workflow_trigger_dao

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.post("/rule", tags=["rule"], include_in_schema=tracardi.expose_gui_api)
async def upsert_rule(rule: Rule):
    """
    Adds new trigger rule to database
    """

    if rule.type == 'event-collect':
        event_source: Optional[EventSource] = await event_source_dao.load_event_source_by_id(rule.source.id)

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

    flow_record = await workflow_dao.load_by_id(rule.flow.id)

    if flow_record is None:
        new_flow = FlowRecord(id=rule.flow.id, name=rule.flow.name, description="", type='collection')
        await workflow_dao.insert(new_flow)
        # await flow_db.save(new_flow)

    return await workflow_trigger_dao.insert(rule)


@router.get("/rule/{id}", tags=["rule"], response_model=Optional[Rule], include_in_schema=tracardi.expose_gui_api)
async def get_rule(id: str, response: Response):
    """
    Returns rule or None if rule does not exist.
    """
    trigger_rule = await workflow_trigger_dao.load_by_id(id)

    if not trigger_rule:
        response.status_code = 404
        return None

    return trigger_rule


@router.delete("/rule/{id}", tags=["rule"], include_in_schema=tracardi.expose_gui_api)
async def delete_rule(id: str):
    """
    Deletes rule with given ID (str) from database
    """
    return await workflow_trigger_dao.delete_by_id(id)


@router.get("/rules/by_flow/{workflow_id}", tags=["rules"], response_model=List[Rule],
            include_in_schema=tracardi.expose_gui_api)
async def get_rules_attached_to_flow(workflow_id: str) -> List[Rule]:
    """
    Returns list of rules attached to flow with given ID (str)
    """
    results, _ = await workflow_trigger_dao.load_by_workflow(workflow_id=workflow_id)
    return results


@router.get("/rules/by_tag", tags=["rules"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_rules_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    """
    Lists rules by tags, according to query (str), start (int) and limit (int) parameters
    """
    records, total = await workflow_trigger_dao.load_all(search=query, offset=start, limit=limit)
    return {
        "total": total,
        "grouped": {
            "Triggers": records
        }
    }


@router.get("/rules/by_event_type/{event_type_id}", tags=["rules"], response_model=dict,
            include_in_schema=tracardi.expose_gui_api)
async def get_rules_by_event_type(event_type_id: str) -> dict:
    """
    Lists rules by event types
    """
    records, total = await workflow_trigger_dao.load_by_event_type(event_type_id=event_type_id)
    return {
        "total": total,
        "result": records
    }
