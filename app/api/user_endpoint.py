from fastapi import APIRouter, Depends, HTTPException
from .auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel, validator
from typing import List, Optional
from uuid import UUID
from elasticsearch import ElasticsearchException
import re


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


class NewUserPayload(UserPayload):
    id: UUID


router = APIRouter(
    dependencies=[
        Depends(get_current_user)
    ]
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
async def add_user(user: NewUserPayload):
    """
    Creates new user in database
    """
    try:
        user_exists = await storage.driver.user.check_if_exists(user.email, user.id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not user_exists:
        try:
            result = await storage.driver.user.add_user(
                id=str(user.id),
                password=user.password,
                full_name=user.full_name,
                email=user.email,
                roles=user.roles,
                disabled=user.disabled
            )
            await storage.driver.user.refresh()
        except ElasticsearchException as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {"inserted": result.saved}
    else:
        raise HTTPException(status_code=409, detail=f"User with email '{user.email}' already exists.")


@router.delete("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_user(id: UUID):
    """
    Deletes user with given ID (uuid4)
    """
    try:
        result = await storage.driver.user.del_user(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Profile with id '{id}' not found")
        await storage.driver.user.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result["result"] == "deleted" else 0}


@router.get("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user(id: UUID):
    """
    Returns user with given ID (uuid4)
    """
    try:
        result = await storage.driver.user.get_by_id(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"User with ID {id} not found.")
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
    return list(map(lambda record: record["_source"] if query else record, result["hits"]["hits"] if
                query else list(result)))


@router.post("/users/{id}/edit", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def edit_user(id: UUID, user: UserPayload):
    """
    Edits existing user with given ID (uuid4)
    """
    try:
        current_user = await storage.driver.user.get_by_id(id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    if current_user:
        try:
            result = await storage.driver.user.edit_user(
                id=str(id),
                password=user.password if user.password != current_user["password"] else current_user["password"],
                full_name=user.full_name,
                email=user.email,
                roles=user.roles,
                disabled=user.disabled,
                password_change=user.password != current_user["password"]
            )
            await storage.driver.user.refresh()
        except ElasticsearchException as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {"inserted": result.saved}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID '{id}' does not exist")
