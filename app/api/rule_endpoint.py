import asyncio
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from tracardi.service.storage.factory import StorageFor, storage

from tracardi.domain.resource import ResourceRecord
from .auth.authentication import get_current_user
from tracardi.domain.entity import Entity
from tracardi.domain.flow import FlowRecord
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.rule import Rule

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/rule/{id}", tags=["rule"], response_model=Rule)
async def get_rule(id: str):
    """
    Returns rule or None if rule does not exist.
    """

    try:
        rule = Entity(id=id)
        return await StorageFor(rule).index("rule").load(Rule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rule", tags=["rule"])
async def upsert_rule(rule: Rule):
    try:
        # Check if source id exists
        entity = Entity(id=rule.source.id)
        resource = await StorageFor(entity).index('resource').load(ResourceRecord)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if resource is None:
        raise HTTPException(status_code=422, detail='Missing source id: `{}`'.format(rule.source.id))

    try:

        entity = Entity(id=rule.flow.id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord
        add_flow_task = None
        if flow_record is None:
            new_flow = NamedEntity(id=rule.flow.id, name=rule.flow.name)
            add_flow_task = asyncio.create_task(StorageFor(entity).index("flow").save(new_flow.dict()))

        add_rule_task = asyncio.create_task(StorageFor(rule).index().save())
        # add_rule_task = asyncio.create_task(rule.storage().save())

        if add_flow_task:
            await add_flow_task
        return await add_rule_task

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/rule/{id}", tags=["rule"])
async def delete_rule(id: str):
    try:
        rule = Entity(id=id)
        return await StorageFor(rule).index("rule").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules/by_flow/{id}", tags=["rules"], response_model=List[Rule])
async def get_rules_attached_to_flow(id: str):
    try:
        rules = storage('rule')

        rules_attached_to_flow = await rules.load_by('flow.id.keyword', id)
        rules = [Rule(**rule) for rule in rules_attached_to_flow]
        return rules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules/refresh", tags=["rules"])
async def refresh_rules():
    service = storage('rule')
    return await service.refresh()
