from fastapi import APIRouter, Depends, HTTPException
from .auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID
from elasticsearch import ElasticsearchException


class UserPayload(BaseModel):
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False


class NewUserPayload(UserPayload):
    id: Optional[UUID] = uuid4()
    username: str


router = APIRouter(
    dependencies=[
        Depends(get_current_user)
    ]
)


@router.post("/user/create", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_user(user: NewUserPayload):
    try:
        user_exists = await storage.driver.user.check_if_exists(user.username, user.id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    if not user_exists:
        try:
            result = await storage.driver.user.add_user(
                id=str(user.id),
                username=user.username,
                password=user.password,
                full_name=user.full_name,
                email=user.email,
                roles=user.roles,
                disabled=user.disabled
            )
        except ElasticsearchException as e:
            raise HTTPException(status_code=500, detail=str(e))
        return {"inserted": result.saved}
    else:
        raise HTTPException(status_code=409, detail=f"User with username '{user.username}' already exists.")


@router.delete("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_user(id: UUID):
    try:
        result = await storage.driver.user.del_user(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Profile with id '{id}' not found")
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result["result"] == "deleted" else 0}

