from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.user_db import token2user
from app.config import server
from pydantic import ValidationError
from app.api.user_endpoint import UserPayload, UserSoftEditPayload

from elasticsearch import ElasticsearchException

from app.service.user_manager import update_user
from tracardi.config import tracardi
from app.api.auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer", "maintainer"]))]
)


@router.get("/user-account", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user_account(user=Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):
    """
    Returns data of the user who called the endpoint
    """
    return user.dict()


@router.post("/user-account", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def edit_user_account(payload: UserSoftEditPayload,
                            user=Depends(Permissions(["admin", "developer", "marketer", "maintainer"]))):

    """
    Edits currently logged user.
    """

    try:

        saved, new_user = await update_user(
            user.id,
            UserPayload(**payload.dict(),
                        roles=user.roles,
                        disabled=user.disabled,
                        email=user.email)
        )

        if tracardi.tokens_in_redis:
            await token2user.set(user.token, new_user)

        return {"inserted": saved}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=403, detail=str(e.raw_errors[0].exc))
