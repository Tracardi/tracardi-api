from typing import Optional

from fastapi import APIRouter, Depends

from tracardi.domain.consent_field_compliance import ConsentFieldCompliance
from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "maintainer"]))]
)


@router.get("/consent/compliance/fields", tags=["compliance"], include_in_schema=server.expose_gui_api)
async def get_field_compliance_with_customer_consent(query: Optional[str] = None, start: int = 0, limit: int = 100):
    result = await storage.driver.data_compliance.load_all(start=start, limit=limit)
    return group_records(result, query, group_by=None, search_by='name', sort_by='name')


@router.post("/consent/compliance/field", tags=["compliance"], include_in_schema=server.expose_gui_api)
async def create_field_compliance_with_customer_consent(compliance_setting: ConsentFieldCompliance):
    result = await storage.driver.data_compliance.upsert(compliance_setting)
    await storage.driver.data_compliance.refresh()
    return result


@router.get("/consent/compliance/field/{id}", tags=["compliance"], include_in_schema=server.expose_gui_api)
async def get_field_compliance_with_customer_consent(id: str):
    return await storage.driver.data_compliance.load_by_id(id)


@router.delete("/consent/compliance/field/{id}", tags=["compliance"], include_in_schema=server.expose_gui_api)
async def delete_field_compliance_with_customer_consent(id: str):
    result = await storage.driver.data_compliance.delete_by_id(id)
    await storage.driver.data_compliance.refresh()
    return result
