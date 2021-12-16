from fastapi import HTTPException
from tracardi.domain.credentials import Credentials
from tracardi.service.microservice import MicroserviceApi

from tracardi.service.storage.driver import storage


async def get_tracardi_pro_services(available=None):
    endpoint = await storage.driver.pro.read_pro_service_endpoint()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="Tracardi Pro services not connected.")

    client = MicroserviceApi(endpoint.url,
                             credentials=Credentials(username=endpoint.username,
                                                     password=endpoint.password))
    path = endpoint.get_running_services_endpoint() \
        if available is None \
        else endpoint.get_available_services_endpoint()

    response = await client.call(path, method="GET")
    if response.status == 200:
        return await response.json()
    return []
