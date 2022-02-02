import grpc
from fastapi import APIRouter, Depends, HTTPException
from google.protobuf import json_format

from app.api.domain.credentials import Credentials
from app.api.proto.tracard_pro_client import TracardiProClient
from tracardi.service.storage.driver import storage

from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi_pro_services_pb2 import Services

router = APIRouter(
    # dependencies=[Depends(get_current_user)]
)

tracardi_pro_client = TracardiProClient(host="localhost", port=12345)


@router.get("/tpro", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def is_authorized():
    """
    Return None if not configured otherwise returns credentials.
    """
    return await storage.driver.pro.read_pro_service_endpoint()


@router.post("/tpro/authorize", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def authorized_tracardi_pro(credentials: Credentials):
    result = tracardi_pro_client.authorize(credentials.username, credentials.password)
    print(credentials)
    print(result)
    if result is True:
        return {
            "username": credentials.username,
            "password": credentials.password
        }

    raise HTTPException(detail="Access denied", status_code=403)  # Must be 403 because 401 logs out gui


@router.get("/tpro/available_services", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    try:
        services = tracardi_pro_client.get_available_services()  # type: Services
        print(services)
        return json_format.MessageToDict(services)

    except grpc.RpcError as e:
        # Must be 403 because 401 logs out gui
        raise HTTPException(detail=e.details(), status_code=403 if e.code().name == 'UNAUTHENTICATED' else 500)
