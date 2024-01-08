from elasticsearch.exceptions import NotFoundError
from fastapi import APIRouter, Depends, HTTPException
from tracardi.service.staging import move_from_staging_to_production, add_alias_staging_to_production, \
    remove_alias_staging_to_production

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/production/deploy", tags=["staging"], include_in_schema=tracardi.expose_gui_api)
async def deploy_staging_to_production():
    """
    Deploys current staging server data to production.
    """
    try:
        return await move_from_staging_to_production()
    except NotFoundError as e:
        raise HTTPException(detail=f"Error: {str(e)}, Reason: Probably production not installed.", status_code=422)


@router.get("/production/dry-run", tags=["staging"], include_in_schema=tracardi.expose_gui_api)
async def dry_run_staging_on_production():
    """
    Connects current staging server data to production. Can be reverted.
    """
    try:
        return await add_alias_staging_to_production()
    except NotFoundError as e:
        raise HTTPException(detail=f"Error: {str(e)}, Reason: Probably production not installed.", status_code=422)


@router.get("/production/dry-run/revert", tags=["staging"], include_in_schema=tracardi.expose_gui_api)
async def disconnect_staging_from_production():
    """
    Revert to old production data.
    """
    try:
        return await remove_alias_staging_to_production()
    except NotFoundError as e:
        raise HTTPException(detail=f"Error: {str(e)}, Reason: Probably production not installed.", status_code=422)
