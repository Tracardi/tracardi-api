from fastapi import APIRouter, HTTPException, Depends
from app.api.auth.authentication import get_current_user
from app.config import server
from tracardi.service.storage.factory import storage_manager

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/storage/mapping/{index}", tags=["storage"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_index_mapping(index: str):
    mapping = await storage_manager(index).get_mapping()
    return mapping.get_field_names()

