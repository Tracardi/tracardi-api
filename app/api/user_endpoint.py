from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Header, Response

from tracardi.context import ServerContext, Context, get_context
from tracardi.domain.user import User
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from typing import Optional, Union

from .auth.permissions import Permissions
from .domain.user_payload import UserPayload
from ..service.user_manager import update_user
from .auth.user_db import token2user
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from .auth.authentication import Authentication, get_authentication


class UserSoftEditPayload(BaseModel):
    password: str
    full_name: str


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)

auth_router = APIRouter()


@auth_router.post("/user/token", tags=["user", "authorization"], include_in_schema=server.expose_gui_api)
async def get_token(login_form_data: OAuth2PasswordRequestForm = Depends(),
                    auth: Authentication = Depends(get_authentication)):
    """
    Returns OAuth2 token for login purposes
    """

    # Always log in the context of staging

    with ServerContext(get_context().switch_context(production=False)):

        if not server.expose_gui_api:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden")

        try:
            token = await auth.login(login_form_data.username, login_form_data.password)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return token


@auth_router.post("/user/logout", tags=["user", "authorization"], include_in_schema=server.expose_gui_api)
async def logout(authorization: Union[str, None] = Header(default=None),
                 auth: Authentication = Depends(get_authentication)):
    """
    Logs out user
    """

    if authorization is None:
        raise HTTPException(status_code=401, detail="No authorization header provided.")

    else:
        _, token = authorization.split(" ")
        auth.logout(token)


@router.get("/user/preference/{key}", tags=["user"], include_in_schema=server.expose_gui_api)
async def get_user_preference(key: str,
                              response: Response,
                              user=Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Returns user preference
    """

    pref = user.preference.get(key, None)

    if pref is None:
        response.status_code = 404
        return None

    return pref


@router.post("/user/preference/{key}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def set_user_preference(key: str, preference: Union[dict, str, int, float],
                              user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Sets user preference.Uses key to set the preference
    """

    user.set_preference(key, preference)
    result = await storage.driver.user.update_user(user)
    await storage.driver.user.refresh()

    token2user.set(user)

    return result


@router.delete("/user/preference/{key}", tags=["user"], include_in_schema=server.expose_gui_api)
async def delete_user_preference(key: str, user=Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Deletes user preference
    """

    if key in user.preference:
        user.delete_preference(key)
        result = await storage.driver.user.update_user(user)

        token2user.set(user)

        return result
    else:
        raise HTTPException(status_code=404, detail=f"Preference {key} not found")


@router.get("/user/preferences", tags=["user"], include_in_schema=server.expose_gui_api, response_model=Optional[dict])
async def gets_all_user_preferences(user=Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Returns all user preferences
    """

    return user.preference


@router.get("/user/refresh", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def refresh_users():
    """
    Refreshes users index
    """

    return await storage.driver.user.refresh()


@router.get("/user/flush", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def flush_users():
    """
    Flushes users index
    """

    return await storage.driver.user.flush()


@router.post("/user", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_user(user_payload: UserPayload):

    """
    Creates new user in database
    """

    user_exists = await storage.driver.user.check_if_exists(user_payload.email)
    if not user_exists:
        expiration_timestamp = user_payload.get_expiration_date()
        result = await storage.driver.user.add_user(
            User(
                **user_payload.dict(),
                id=str(uuid4()),
                expiration_timestamp=expiration_timestamp
            )
        )
        await storage.driver.user.refresh()

        return result
    else:
        raise HTTPException(status_code=409, detail=f"User with email '{user_payload.email}' already exists.")


@router.delete("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_user(id: str, user=Depends(Permissions(["admin"]))):
    """
    Deletes user with given ID
    """

    if id == user.id:
        raise HTTPException(status_code=403, detail="You cannot delete your own account")
    result = await storage.driver.user.delete_user(id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"User '{id}' not found")
    await storage.driver.user.refresh()

    return {"deleted": 1 if result["result"] == "deleted" else 0}


@router.get("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user(id: str):
    """
    Returns user with given ID
    """

    record = await storage.driver.user.load_by_id(id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found.")

    if 'token' in record:
        del record['token']

    return record


@router.get("/users/{start}/{limit}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_users(start: int = 0, limit: int = 100, query: Optional[str] = ""):
    """
    Lists users according to given query (str), start (int) and limit (int) parameters
    """

    return await storage.driver.user.search_by_name(start, limit, query)


@router.post("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def edit_user(id: str, user_payload: UserPayload, user=Depends(Permissions(["admin"]))):
    """
    Edits existing user with given ID
    """

    if user.is_the_same_user(id) and not user_payload.has_admin_role() and user.is_admin():
        raise HTTPException(status_code=403, detail="You cannot remove the role of admin from your own account")

    try:
        saved, updated_user = await update_user(id, user_payload)
        token2user.set(updated_user)
        return {"inserted": saved}

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
