import grpc
from fastapi import APIRouter, Depends, HTTPException
from google.protobuf import json_format

from app.api.proto.tracard_pro_client import TracardiProClient
from tracardi.service.storage.driver import storage

from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi_pro_services_pb2 import ServiceDescriptionDict

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

tracardi_pro_client = TracardiProClient(host="localhost", port=12345)


@router.get("/tpro", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def is_authorized():
    """
    Return None if not configured otherwise returns credentials.
    """
    return await storage.driver.pro.read_pro_service_endpoint()


@router.get("/tpro/authorize", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def authorized_tracardi_pro(username: str, password: str):
    result = tracardi_pro_client.authorize(username, password)
    print(result)
    return result


@router.get("/tpro/available_services", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    try:
        service_description_dict = tracardi_pro_client.get_available_services()  # type: ServiceDescriptionDict
        return json_format.MessageToDict(service_description_dict)

    except grpc.RpcError as e:
        raise HTTPException(detail=e.details(), status_code=401 if e.code().name == 'UNAUTHENTICATED' else 500)