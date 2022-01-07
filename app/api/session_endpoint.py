from typing import Optional
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.storage.factory import StorageFor, storage_manager
from tracardi.service.wf.domain.entity import Entity
from .auth.authentication import get_current_user
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/session/{id}",
            tags=["session"],
            response_model=Optional[Session],
            include_in_schema=server.expose_gui_api)
async def get_profile_by_id(id: str, response: Response):
    try:
        result = await storage_manager("session").load(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404

    return result
