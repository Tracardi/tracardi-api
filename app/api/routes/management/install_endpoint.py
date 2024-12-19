from typing import Optional
from fastapi import APIRouter, HTTPException

from tracardi.domain.installation_status import SystemInstallationStatus
from tracardi.service.installation import install_system
from tracardi.config import tracardi
from tracardi.domain.credentials import Credentials
from tracardi.service.setup.setup_envs import get_system_envs

router = APIRouter()


@router.get("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=SystemInstallationStatus)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """
    status = await SystemInstallationStatus.check()

    status.config = get_system_envs()

    return status


@router.post("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install(credentials: Optional[Credentials]):

    try:
        return await install_system(credentials)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))




