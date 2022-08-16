from fastapi import APIRouter, Header
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Union

from .auth.authentication import Authentication, get_authentication
from ..config import server

router = APIRouter()


@router.post("/token", tags=["authorization"], include_in_schema=server.expose_gui_api)
async def login(login_form_data: OAuth2PasswordRequestForm = Depends(),
                auth: Authentication = Depends(get_authentication)):
    """
    Returns OAuth2 token for login purposes
    """
    if not server.expose_gui_api:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden")

    # try:
    token = await auth.login(login_form_data.username, login_form_data.password)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=str(e))

    return token


@router.post("/logout", tags=["authorization"], include_in_schema=server.expose_gui_api)
async def logout(authorization: Union[str, None] = Header(default=None),
                 auth: Authentication = Depends(get_authentication)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="No authorization header provided.")

    else:
        try:
            _, token = authorization.split(" ")
            await auth.logout(token)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



