from fastapi import APIRouter, HTTPException, Depends

from app.api.auth.permissions import Permissions
from tracardi.event_server.utils.memory_cache import MemoryCache, CacheItem
from app.config import server
from tracardi.service.storage.factory import storage_manager

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)

memory_cache = MemoryCache()


@router.get("/storage/mapping/{index}/metadata", tags=["storage"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_index_mapping(index: str):
    """
    Returns metadata of given index (str)
    """
    try:
        memory_key = f"{index}-mapping-cache"
        if memory_key not in memory_cache:
            mapping = await storage_manager(index).get_mapping()
            fields = mapping.get_field_names()
            memory_cache[memory_key] = CacheItem(data=fields, ttl=5)  # result is cached for 5 seconds
        return {"result": memory_cache[memory_key].data, "total": len(memory_cache[memory_key].data)}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


@router.get("/storage/mapping/{index}", tags=["storage"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_index_mapping(index: str):
    """
    Returns mapping of given index (str)
    """
    try:
        mapping = await storage_manager(index).get_mapping()
        return mapping.get_field_names()
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)
