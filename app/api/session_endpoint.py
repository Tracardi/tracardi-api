from typing import Optional, List
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response
from tracardi.domain.session import Session
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import storage_manager
from .auth.authentication import get_current_user
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/sessions/refresh", tags=["session"], include_in_schema=server.expose_gui_api)
async def session_refresh():
    return await storage.driver.session.refresh()


@router.post("/sessions/import", tags=["session"], include_in_schema=server.expose_gui_api)
async def import_profiles(sessions: List[Session]):
    try:
        return await storage.driver.session.save_sessions(sessions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{id}",
            tags=["session"],
            response_model=Optional[Session],
            include_in_schema=server.expose_gui_api)
async def get_session_by_id(id: str, response: Response):
    try:
        result = await storage_manager("session").load(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404

    return result


@router.delete("/session/{id}", tags=["session"], include_in_schema=server.expose_gui_api)
async def delete_session(id: str, response: Response):

    # try:
    result = await storage.driver.session.delete(id)
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result
