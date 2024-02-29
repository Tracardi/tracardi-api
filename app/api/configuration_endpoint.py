from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.service.grouping import get_grouped_result
from tracardi.domain.configuration import Configuration
from tracardi.service.setup.setup_configuration import available_configuration_list
from tracardi.service.storage.mysql.mapping.configuration_mapping import map_to_configuration
from tracardi.service.storage.mysql.service.configuration_service import ConfigurationService

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer", "developer"]))]
)

cs = ConfigurationService()

@router.get("/configuration/{id}", tags=["configuration"], include_in_schema=tracardi.expose_gui_api)
async def get_configuration(id: str):
    record = await cs.load_by_id(id)
    if not record.exists():
        raise HTTPException(status_code=404, detail=f"Configuration with ID {id} not found.")

    return record.map_to_object(map_to_configuration)


@router.get("/configuration", tags=["configuration"], include_in_schema=tracardi.expose_gui_api)
async def list_defined_configuration(query: Optional[str] = None, limit: int = 200):
    records = await cs.load_all(search=query, limit=limit)

    return get_grouped_result("Configuration Settings", records, map_to_configuration)


@router.post("/configuration", tags=["configuration"], include_in_schema=tracardi.expose_gui_api)
async def add_configuration(config: Configuration):
    return await cs.upsert(config)


@router.delete("/configuration/{id}", tags=["configuration"], include_in_schema=tracardi.expose_gui_api)
async def delete_configuration(id: str):
    """
    Deletes configuration from the database
    """
    return await cs.delete_by_id(id)

# Lists

@router.get("/configuration-type", tags=["configuration"], include_in_schema=tracardi.expose_gui_api)
async def list_configuration_types():
    return {
        "total": len(available_configuration_list),
        "result": list(available_configuration_list.values())
    }