from fastapi import APIRouter
from app.config import server
from tracardi.service.storage.drivers.elastic import raw

router = APIRouter()


@router.get("/purchases/plugin/{profile_id}", tags=["purchases"], include_in_schema=server.expose_gui_api)
async def get_purchases_by_id(profile_id: str) -> list:
    purchases_amount = (await raw.index("profile-purchase").storage.search({
        "query": {
            "bool": {
                "must": [
                    {"match": {"profile.id": profile_id}}
                ]
            }
        }
    }))["hits"]["total"]["value"]
    purchases = (await raw.index("profile-purchase").storage.load_by(
        "profile.id",
        profile_id,
        purchases_amount
    ))
    return purchases["hits"]["hits"]
