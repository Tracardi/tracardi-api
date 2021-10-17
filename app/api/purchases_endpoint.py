from fastapi import APIRouter
from app.config import server
from tracardi.service.storage.drivers.elastic import raw

router = APIRouter()


@router.get("/purchases/plugin/{profile_id}", tags=["purchases"], include_in_schema=server.expose_gui_api)
async def get_purchases_by_id(profile_id: str, limit: int = 0) -> list:
    purchases = (await raw.index("profile-purchase").storage.load_by(
        "profile.id",
        profile_id,
        limit if 0 < limit < 1000 else 10
    ))["hits"]["hits"]
    return purchases
