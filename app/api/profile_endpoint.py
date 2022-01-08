from typing import List, Optional

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from .auth.authentication import get_current_user
from tracardi.domain.profile import Profile
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/profiles/import", tags=["profile"], include_in_schema=server.expose_gui_api)
async def import_profiles(profiles: List[Profile]):
    try:
        return await storage.driver.profile.save_profiles(profiles)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profiles/refresh", tags=["profile"], include_in_schema=server.expose_gui_api)
async def refresh_profile():
    try:
        return await storage.driver.profile.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{id}", tags=["profile"], response_model=Profile, include_in_schema=server.expose_gui_api)
async def get_profile_by_id(id: str, response: Response):
    try:
        profile = Profile(id=id)
        result = await StorageFor(profile).index().load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404

    return result


@router.delete("/profile/{id}", tags=["profile"], response_model=Optional[dict], include_in_schema=server.expose_gui_api)
async def delete_profile(id: str, response: Response):
    try:
        result = await storage.driver.profile.delete(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result['deleted'] == 0:
        response.status_code = 404
        return None

    return result


@router.get("/profile/logs/{id}", tags=["profile"], response_model=list, include_in_schema=server.expose_gui_api)
async def get_profile_logs(id: str):
    log_records = await storage.driver.console_log.load_by_profile(id)
    return list(log_records)
