from fastapi import APIRouter, Depends

from com_tracardi.service.mysql.deployment_service import DeploymentService
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/deploy/{table_name}/{id}", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def deploy_object(table_name: str, id: str):
    ds = DeploymentService(True)
    return await ds.deploy(table_name, id, deploy=True)


@router.get("/undeploy/{table_name}/{id}", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def undeploy_object(table_name: str, id: str):
    ds = DeploymentService(True)
    return await ds.deploy(table_name, id, deploy=False)
