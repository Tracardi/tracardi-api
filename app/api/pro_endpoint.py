from typing import Optional

from asyncio import sleep
from fastapi import APIRouter, HTTPException, Depends

from app.service.tracardi_pro_inbound_sources import get_tracardi_pro_services
from tracardi.domain.credentials import Credentials
from tracardi.domain.pro_service_config import TracardiProServiceConfig

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
async def set_tracardi_pro_endpoint(endpoint: TracardiProEndpoint):
    try:
        result = await storage.driver.pro.save_pro_service_endpoint(endpoint)

        if result.saved == 0:
            raise HTTPException(status_code=500, detail="Could not save Tracardi Pro endpoint.")

        client = MicroserviceApi(endpoint.url,
                                 credentials=Credentials(username=endpoint.username,
                                                         password=endpoint.password))
        response = await client.call(endpoint.get_available_services_endpoint(), method="GET")
        if response.status == 200:
            return endpoint
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@router.delete("/tracardi-pro", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    return await storage.driver.pro.delete_pro_service_endpoint()


@router.put("/tracardi-pro/services", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def refresh_configured_tracardi_pro_services():
    endpoint = await storage.driver.pro.read_pro_service_endpoint()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Tracardi Pro services not connected.")

    client = MicroserviceApi(endpoint.url,
                             credentials=Credentials(username=endpoint.username,
                                                     password=endpoint.password))

    response = await client.call(endpoint.get_running_services_endpoint(), method="PUT")
    if response.status == 200:
        return await response.json()
    return []


@router.get("/tracardi-pro/services", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_configured_tracardi_pro_services(available: Optional[str] = None):
    endpoint = await storage.driver.pro.read_pro_service_endpoint()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Tracardi Pro services not connected.")
    return await get_tracardi_pro_services(endpoint, available)


@router.delete("/tracardi-pro/service/{id}", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def delete_tracardi_pro_service(id: str):
    endpoint = await storage.driver.pro.read_pro_service_endpoint()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Tracardi Pro services not connected.")

    client = MicroserviceApi(endpoint.url,
                             credentials=Credentials(username=endpoint.username,
                                                     password=endpoint.password))

    response = await client.call(endpoint.get_running_service(id), method="DELETE")
    if response.status == 200:
        return await response.json()
    return []


@router.get("/tracardi-pro/service/{id}/actions", tags=["tracardi-pro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_service_actions(id: str):
    resource = await storage.driver.resource.load(id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource {} not available.".format(id))

    config = TracardiProServiceConfig(**resource.credentials.production)
    client = MicroserviceApi(config.auth.url,
                             credentials=Credentials(username=config.auth.username,
                                                     password=config.auth.password))

    response = await client.call(config.services, method="GET")
    if response.status == 200:
        return await response.json()
    return []
