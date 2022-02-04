from uuid import uuid4

import grpc
from fastapi import APIRouter, Depends, HTTPException

from app.api.domain.credentials import Credentials
from tracardi.domain.sign_up_data import SignUpData
from app.api.proto.tracard_pro_client import TracardiProClient
from tracardi.service.storage.driver import storage

from app.api.auth.authentication import get_current_user
from app.config import server
from app.api.proto.stubs.tracardi_pro_services_pb2 import Services

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

tracardi_pro_client = TracardiProClient(host="localhost", port=12345)


@router.get("/tpro/validate", tags=["tpro"], include_in_schema=server.expose_gui_api, response_model=bool)
async def is_token_valid():
    """
    Return None if not configured otherwise returns True if credentials are valid or False.
    """
    result = await storage.driver.pro.read_pro_service_endpoint()

    if result is None:
        return None

    token = tracardi_pro_client.validate(token=result.token)

    return False
    return token is not None


@router.post("/tpro/sign_in", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def tracardi_pro_sigh_in(credentials: Credentials):
    try:
        tracardi_pro_client.sign_in(credentials.username, credentials.password)
        return True
    except PermissionError as e:
        raise HTTPException(detail="Access denied due to {}".format(str(e)),
                            status_code=403)  # Must be 403 because 401 logs out gui
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=403)  # Must be 403 because 401 logs out gui


@router.post("/tpro/sign_up", tags=["tpro"], include_in_schema=server.expose_gui_api, response_model=bool)
async def tracardi_pro_sign_up(sign_up_data: SignUpData):
    try:
        token = tracardi_pro_client.sign_up(sign_up_data.username, sign_up_data.password)
        sign_up_data.token = token

        sign_up_data.id = "0"
        result = await storage.driver.pro.save_pro_service_endpoint(sign_up_data)

        if result.saved == 0:
            raise HTTPException(status_code=500, detail="Could not save Tracardi Pro endpoint.")

        return True

    except grpc.RpcError as e:
        raise HTTPException(detail="Access denied due to RPC error \"{}\". Error status: {}".format(e.details(), e.code().name),
                            status_code=403)  # Must be 403 because 401 logs out gui
    except Exception as e:
        raise HTTPException(status_code=500, detail=repr(e))


@router.get("/tpro/available_services", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    try:
        return tracardi_pro_client.get_available_services()  # type: Services

    except grpc.RpcError as e:
        # Must be 403 because 401 logs out gui
        raise HTTPException(detail=e.details(), status_code=403 if e.code().name == 'UNAUTHENTICATED' else 500)


@router.get("/tpro/available_hosts", tags=["tpro"], include_in_schema=server.expose_gui_api)
async def get_tracardi_pro_endpoint():
    try:
        return tracardi_pro_client.get_available_hosts()  # type: Services

    except grpc.RpcError as e:
        # Must be 403 because 401 logs out gui
        raise HTTPException(detail=e.details(), status_code=403 if e.code().name == 'UNAUTHENTICATED' else 500)