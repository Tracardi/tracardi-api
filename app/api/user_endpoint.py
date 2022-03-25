from fastapi import APIRouter, Depends, HTTPException
from tracardi.domain.user import User
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel, validator
from typing import List, Optional

from elasticsearch import ElasticsearchException
import re

from .auth.permissions import Permissions


class UserPayload(BaseModel):
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False

    @validator("email")
    def validate_email(cls, value):
        if not re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', value):
            raise ValueError("Given email is invalid.")
        return value


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
    try:
        user_exists = await storage.driver.user.check_if_exists(user_payload.email)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not user_exists:
        try:

            result = await storage.driver.user.add_user(User(**user_payload.dict(), id=user_payload.email))
            await storage.driver.user.refresh()

        except ElasticsearchException as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"inserted": result.saved}
    else:
        raise HTTPException(status_code=409, detail=f"User with email '{user_payload.email}' already exists.")


@router.delete("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_user(id: str):
    """
    Deletes user with given ID
    """
    try:
        result = await storage.driver.user.delete_user(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"User '{id}' not found")
        await storage.driver.user.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result["result"] == "deleted" else 0}


@router.get("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user(id: str):
    """
    Returns user with given ID
    """
    try:
        result = await storage.driver.user.get_by_id(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"User {id} not found.")
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return UserPayload(**result)


@router.get("/users/{start}/{limit}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_users(start: int = 0, limit: int = 100, query: Optional[str] = ""):
    """
    Lists users according to given query (str), start (int) and limit (int) parameters
    """
    try:
        result = await storage.driver.user.search_by_name(start, limit, query) if query else \
            await storage.driver.user.load(start, limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Todo this is nightmare. Records form database must be validated. Driver can not return elastic structure.
    # Todo this tech debt must be removed
    return list(map(lambda record: record["_source"] if query else record, result["hits"]["hits"] if
    query else list(result)))


@router.post("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def update_user(id: str, user_payload: UserPayload):
    """
    Edits existing user with given ID
    """
    try:
        current_user = await storage.driver.user.get_by_id(id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))

    if current_user:
        try:
            user = User(**user_payload.dict(), id=user_payload.email)

            if user_payload.password != current_user["password"]:
                user.encode_password()

            result = await storage.driver.user.update_user(user)
            await storage.driver.user.refresh()

        except ElasticsearchException as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {"inserted": result.saved}
    else:
        raise HTTPException(status_code=404, detail=f"User '{id}' does not exist")
