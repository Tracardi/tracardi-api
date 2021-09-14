from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.responses import Response

from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from .auth.authentication import get_current_user
from tracardi.domain.profile import Profile

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/profiles/refresh", tags=["profile"])
async def refresh_profile():
    try:
        return await storage.driver.profiles.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{id}", tags=["profile"], response_model=Profile)
async def get_profile_by_id(id: str, response: Response):
    try:
        profile = Profile(id=id)
        result = await StorageFor(profile).index().load()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404

    return result


@router.delete("/profile/{id}", tags=["profile"], response_model=dict)
async def delete_profile(id: str):
    try:
        profile = Profile(id=id)
        return await StorageFor(profile).index().delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/logs/{id}", tags=["profile"], response_model=list)
async def get_profile_logs(id: str):
    log_records = await storage.driver.console_log.load_by_profile(id)
    return list(log_records)
