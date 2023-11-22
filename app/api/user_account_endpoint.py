from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.user_db import token2user
from tracardi.config import tracardi
from pydantic import ValidationError
from app.api.user_endpoint import UserPayload, UserSoftEditPayload

from app.api.auth.permissions import Permissions
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


@router.post("/user-account", tags=["user"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def edit_user_account(payload: UserSoftEditPayload,
                            user: User = Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Edits currently logged user.
    """

    try:

        existing_user = user.model_copy()
        if payload.password:
            existing_user.password = User.encode_password(payload.password)

        if payload.full_name:
            existing_user.full_name = payload.full_name

        us = UserService()

        saved, new_user = await us.update_if_exist(
            user.id,
            UserPayload(
                full_name=existing_user.full_name,
                password=existing_user.password,
                roles=existing_user.roles,
                disabled=existing_user.disabled,
                email=existing_user.email)
        )

        token2user.set(new_user)

        return {"inserted": saved}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=403, detail=str(e.raw_errors[0].exc))
