from fastapi import APIRouter, Depends
from tracardi.config import tracardi
from tracardi.context import get_context
from tracardi.service.decorators.function_memory_cache import cache
from tracardi.service.tracking.cache.cache_helper import _ttl, _get_cache
from tracardi.service.tracking.cache.flat_profile_cache import get_flat_profile_key_namespace
from tracardi.service.tracking.cache.session_cache import get_session_key_namespace
from app.api.auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))]
)


@router.get("/cache/profile/expire", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_profile_cache_ttl(profile_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_flat_profile_key_namespace(profile_id, get_context())
    return {
        "ttl": _ttl(profile_id, namespace),
        "namespace": namespace
    }


@router.get("/cache/session/expire", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_session_cache_ttl(session_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_session_key_namespace(session_id, get_context())
    return {"ttl": _ttl(session_id, namespace)}


@router.get("/cache/profile", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_profile_data(profile_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_flat_profile_key_namespace(profile_id, get_context())
    return {"profile": _get_cache(profile_id, namespace)}


@router.get("/cache/session", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_session_data(session_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_session_key_namespace(session_id, get_context())
    return {"session": _get_cache(session_id, namespace)}


@router.get("/cache/memory/count", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_memory_cache_count():
    """
    Returns memory cache count.
    """
    return {
        "cache": {
            "size": len(cache),
            "keys": [(key, item.get_cached_items()) for key, item in cache.items()]
        }
    }
