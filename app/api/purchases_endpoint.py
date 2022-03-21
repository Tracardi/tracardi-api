from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.service.storage.driver import storage

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


# todo can not find usage of this endpoint

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
