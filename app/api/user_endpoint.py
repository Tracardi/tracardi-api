from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Header, Response

from tracardi.context import ServerContext, get_context
from tracardi.domain.user import User
from tracardi.config import tracardi
from pydantic import BaseModel
from typing import Optional, Union

from tracardi.service.storage.mysql.mapping.user_mapping import map_to_user
from tracardi.service.storage.mysql.schema.table import UserTable
from tracardi.service.storage.mysql.service.user_service import UserService
from .auth.permissions import Permissions
from tracardi.domain.user_payload import UserPayload
from .auth.user_db import token2user
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from .auth.authentication import Authentication, get_authentication
from ..service.grouping import get_grouped_result


class UserSoftEditPayload(BaseModel):
    password: Optional[str] = None
    name: Optional[str] = None


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)

auth_router = APIRouter()
# logger = get_logger(__name__)

@auth_router.post("/user/token",
                  tags=["user", "authorization"],
                  include_in_schema=tracardi.expose_gui_api)
async def get_token(login_form_data: OAuth2PasswordRequestForm = Depends(),
                    auth: Authentication = Depends(get_authentication)):
    """
    Returns OAuth2 token for login purposes
    """

    # Always log in the context of staging

    with ServerContext(get_context().switch_context(production=False)):

        if not tracardi.expose_gui_api:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access forbidden")

        try:
            token = await auth.login(login_form_data.username, login_form_data.password)
        except Exception as e:
            message = f"Authentication error: {str(e)}"
            # logger.error(message)
            raise HTTPException(status_code=400, detail=message)

        return token


@auth_router.post("/user/logout", tags=["user", "authorization"], include_in_schema=tracardi.expose_gui_api)
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


@router.get("/user/preference/{key}", tags=["user"], include_in_schema=tracardi.expose_gui_api)
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


@router.post("/user/preference/{key}",
             tags=["user"],
             include_in_schema=tracardi.expose_gui_api)
async def set_user_preference(key: str, preference: Union[dict, str, int, float],
                              user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Sets user preference.Uses key to set the preference
    """

    user.set_preference(key, preference)

    us = UserService()
    result = await us.upsert(user)

    # result = await user_db.update_user(user)
    # await user_db.refresh()

    token2user.set(user)

    return result


@router.delete("/user/preference/{key}", tags=["user"], include_in_schema=tracardi.expose_gui_api)
async def delete_user_preference(key: str,
                                 user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Deletes user preference
    """

    if key in user.preference:
        user.delete_preference(key)

        us = UserService()
        result = await us.upsert(user)

        token2user.set(user)

        return result
    else:
        raise HTTPException(status_code=404, detail=f"Preference {key} not found")


@router.get("/user/preferences", tags=["user"], include_in_schema=tracardi.expose_gui_api,
            response_model=Optional[dict])
async def gets_all_user_preferences(user: User =Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Returns all user preferences
    """

    return user.preference


@router.post("/user", tags=["user"],
             include_in_schema=tracardi.expose_gui_api)
async def add_user(user_payload: UserPayload):
    """
    Creates new user in database
    """

    expiration_timestamp = user_payload.get_expiration_date()
    user = User(
        **user_payload.model_dump(),
        id=str(uuid4()),
        expiration_timestamp=expiration_timestamp
    )

    user.password = User.encode_password(user.password)

    us = UserService()

    user_id = await us.insert_if_none(user)

    if user_id is None:
        raise HTTPException(status_code=409, detail=f"User with email '{user_payload.email}' already exists.")

    return user_id


@router.delete("/user/{id}", tags=["user"], include_in_schema=tracardi.expose_gui_api)
async def delete_user(id: str, user: User=Depends(Permissions(["admin"]))):
    """
    Deletes user with given ID
    """

    if id == user.id:
        raise HTTPException(status_code=403, detail="You cannot delete your own account")

    us = UserService()
    return await us.delete_by_id(id)


@router.get("/user/{id}", tags=["user"], include_in_schema=tracardi.expose_gui_api)
async def get_user(id: str):
    """
    Returns user with given ID
    """
    us = UserService()
    record = await us.load_by_id(id)

    if not record.exists():
        raise HTTPException(status_code=404, detail=f"User {id} not found.")

    if record.has_multiple_records():
        raise HTTPException(status_code=500, detail=f"User {id} has multiple rows in database.")

    user_table: UserTable = record.rows
    user_table.password = None

    return user_table

@router.get("/users", tags=["user"], include_in_schema=tracardi.expose_gui_api)
async def get_users(start: int = 0, limit: int = 500, query: Optional[str] = ""):
    """
    Lists users according to given query (str), start (int) and limit (int) parameters
    """

    us = UserService()
    result = await us.load_all(query, limit, start)

    return get_grouped_result("Users", result, map_to_user)


# TODO remove in 1.0.0
@router.get("/users/{start}/{limit}", tags=["user"], include_in_schema=tracardi.expose_gui_api, response_model=list)
async def get_users(start: int = 0, limit: int = 500, query: Optional[str] = ""):
    """
    Lists users according to given query (str), start (int) and limit (int) parameters
    """

    us = UserService()
    if len(query) > 0:
        users = await us.load_by_name(query, limit, start)
    else:
        users = (await us.load_all(limit, start)).map_to_objects(map_to_user)

    result = []
    for user in users:
        result.append({**user.model_dump(), "expired": user.is_expired()})

    return result

@router.post("/user/{id}", tags=["user"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def edit_user(id: str, user_payload: UserPayload, user=Depends(Permissions(["admin"]))):
    """
    Edits existing user with given ID
    """

    if user.is_the_same_user(id) and not user_payload.has_admin_role() and user.is_admin():
        raise HTTPException(status_code=403, detail="You cannot remove the role of admin from your own account")

    try:

        if user_payload.password and user_payload.password.strip() != "":
            user_payload.password = user_payload.password
        else:
            user_payload.password = None

        us = UserService()

        saved, updated_user = await us.update_if_exist(id, user_payload)
        token2user.set(updated_user)
        return {"inserted": saved}

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
