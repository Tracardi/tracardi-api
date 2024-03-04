from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from app.api.auth.user_db import token2user
from app.api.user_endpoint import UserSoftEditPayload
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.domain.user_payload import UserPayload

from tracardi.domain.user import User
from tracardi.service.storage.mysql.service.user_service import UserService

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer", "maintainer"]))]
)


@router.get("/user-account", tags=["user"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_user_account(user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Returns data of the user who called the endpoint
    """
    return user.model_dump(mode='json', exclude={"password": ...})


@router.post("/user-account", tags=["user"], include_in_schema=tracardi.expose_gui_api)
async def edit_user_account(payload: UserSoftEditPayload,
                            user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Edits currently logged user.
    """

    try:
        existing_user = user.model_copy()

        if payload.password and payload.password.strip()  != "":
            password = payload.password
        else:
            password = None

        if payload.name:
            existing_user.name = payload.name

        us = UserService()

        saved, new_user = await us.update_if_exist(
            user.id,
            UserPayload(
                name=existing_user.name,
                password=password,  # None password will leave old one
                roles=existing_user.roles,
                enabled=existing_user.enabled,
                email=existing_user.email
            )
        )

        token2user.set(new_user)

        return {"inserted": saved}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=403, detail=str(e.raw_errors[0].exc))
