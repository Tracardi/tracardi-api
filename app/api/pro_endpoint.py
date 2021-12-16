from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Depends
from tracardi.domain.credentials import Credentials

from tracardi.service.microservice import MicroserviceApi

from tracardi.domain.tracardi_pro_endpoint import TracardiProEndpoint
from tracardi.service.storage.driver import storage

from app.api.auth.authentication import get_current_user
from app.config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/tracardi-pro", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    return await storage.driver.pro.read_pro_service_endpoint()


@router.post("/tracardi-pro", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint(endpoint: TracardiProEndpoint):
    return await storage.driver.pro.save_pro_service_endpoint(endpoint)


@router.delete("/tracardi-pro", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    return await storage.driver.pro.delete_pro_service_endpoint()


@router.get("/tracardi-pro/services", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_configured_tracardi_pro_services(available: Optional[str] = None):
    endpoint = await storage.driver.pro.read_pro_service_endpoint()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Tracardi Pro services not connected.")

    client = MicroserviceApi(endpoint.url,
                             credentials=Credentials(username=endpoint.username,
                                                     password=endpoint.password))
    path = endpoint.get_registered_services_endpoint() if available is None else endpoint.get_available_services_endpoint()
    response = await client.call(path, method="GET")
    if response.status == 200:
        return await response.json()
    return []


