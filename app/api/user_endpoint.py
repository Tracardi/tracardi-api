from fastapi import APIRouter, Depends, HTTPException
from tracardi.domain.user import User
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from typing import Optional

from .auth.permissions import Permissions
from .domain.user_payload import UserPayload
from ..service.user_manager import update_user
from .auth.user_db import token2user


class UserSoftEditPayload(BaseModel):
    password: str
    full_name: str


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


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
        result = await storage.driver.user.add_user(User(
            **user_payload.dict(),
            id=user_payload.email,
            expiration_timestamp=expiration_timestamp
        ))
        await storage.driver.user.refresh()

        return {"inserted": result.saved}
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
    result = await storage.driver.user.get_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found.")

    return result.dict(exclude={"token"})


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
        token2user.update_user(updated_user)

        return {"inserted": saved}

    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
