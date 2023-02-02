from fastapi import APIRouter, Depends
from tracardi.service.staging import move_from_staging_to_production, add_alias_staging_to_production, \
    remove_alias_staging_to_production

from app.api.auth.permissions import Permissions
from app.config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)


@router.get("/production/deploy", tags=["staging"], include_in_schema=server.expose_gui_api)
async def deploy_staging_to_production():
    """
    Deploys current staging server data to production.
    """

    return await move_from_staging_to_production()


@router.get("/production/dry-run", tags=["staging"], include_in_schema=server.expose_gui_api)
async def dry_run_staging_on_production():
    """
    Connects current staging server data to production. Can be reverted.
    """

    return await add_alias_staging_to_production()


@router.get("/production/dry-run/revert", tags=["staging"], include_in_schema=server.expose_gui_api)
async def disconnect_staging_from_production():
    """
    Revert to old production data.
    """

    return await remove_alias_staging_to_production()
