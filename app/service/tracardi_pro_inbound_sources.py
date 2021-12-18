from tracardi.domain.credentials import Credentials
from tracardi.service.microservice import MicroserviceApi


async def get_tracardi_pro_services(endpoint, available=None):
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
