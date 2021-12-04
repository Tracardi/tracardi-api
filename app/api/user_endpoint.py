from fastapi import APIRouter, Depends, HTTPException
from .auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.driver import storage
from pydantic import BaseModel
from typing import List, Optional
from tracardi.domain.user import User
from uuid import uuid4, UUID
from hashlib import sha1
from elasticsearch import ElasticsearchException


class UserForm(BaseModel):
    id: Optional[str] = uuid4()
    username: str
    password: str
    full_name: str
    email: str
    roles: List[str]
    disabled: bool = False

    def encode(self, salt: str) -> User:
        return User(
            id=self.id,
            username=sha1((salt + self.username).encode()).hexdigest(),
            password=sha1((salt + self.password).encode()).hexdigest(),
            full_name=self.full_name,
            email=self.email,
            roles=self.roles,
            disabled=self.disabled
        )


router = APIRouter(
    dependencies=[
        Depends(get_current_user)
    ]
)


@router.post("/user", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_user(user: UserForm):
    try:
        result = await storage.driver.user.add_user(user)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"inserted": result["saved"]}


@router.delete("/user/{id}", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_user(id: UUID):
    try:
        result = await storage.driver.user.del_user(id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Profile with id '{id}' not found")
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if "deleted" in result else 0}

