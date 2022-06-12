from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from pydantic import ValidationError
from app.api.user_endpoint import UserPayload, UserSoftEditPayload

from elasticsearch import ElasticsearchException

from tracardi.config import tracardi
from .auth.permissions import Permissions
from ..service.user_manager import update_user

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))]
)


@router.get("/user-account", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_user_account(user=Depends(Permissions(["admin", "developer", "marketer"]))):
    """
    Returns data of the user who called the endpoint
    """
    return user.dict()


@router.post("/user-account", tags=["user"], include_in_schema=server.expose_gui_api, response_model=dict)
async def edit_user_account(payload: UserSoftEditPayload,
                            user=Depends(Permissions(["admin", "developer", "marketer"]))):
    try:

        saved = await update_user(user.id,
                                  UserPayload(**payload.dict(),
                                              roles=user.roles,
                                              disabled=user.disabled,
                                              email=user.email)
                                  )

        return {"inserted": saved}
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=403, detail=str(e.raw_errors[0].exc))
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
