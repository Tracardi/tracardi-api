from fastapi import APIRouter, Depends
from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.factory import StorageForBulk

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/action/plugins", include_in_schema=server.expose_gui_api)
async def plugins():
    return await StorageForBulk().index('action').load()
