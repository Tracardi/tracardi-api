from fastapi import APIRouter, Depends

from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.driver import storage

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/purchases/profile/{profile_id}", tags=["purchases"],
            include_in_schema=server.expose_gui_api, response_model=dict)
async def get_purchases_by_id(profile_id: str, limit: int = 0) -> dict:
    """
    Deprecated for now
    """
    return await storage.driver.purchase.load(
        profile_id,
        limit
    )
