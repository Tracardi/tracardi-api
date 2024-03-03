from fastapi import APIRouter, Depends
from tracardi.config import tracardi
from tracardi.context import get_context
from tracardi.service.storage.redis.cache import RedisCache
from tracardi.service.tracking.cache.profile_cache import get_profile_key_namespace
from tracardi.service.tracking.cache.session_cache import get_session_key_namespace
from .auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer","marketer"]))]
)
redis_cache = RedisCache(ttl=None)


@router.get("/cache/profile/expire", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_profile_cache_ttl(profile_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_profile_key_namespace(profile_id, get_context())
    return {
        "ttl" : redis_cache.get_ttl(profile_id, namespace),
        "namespace": namespace
    }


@router.get("/cache/session/expire", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_session_cache_ttl(session_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_session_key_namespace(session_id, get_context())
    return {"ttl" : redis_cache.get_ttl(session_id, namespace)}


@router.get("/cache/profile", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_profile_data(profile_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_profile_key_namespace(profile_id, get_context())
    return {"profile" : redis_cache.get(profile_id, namespace)}


@router.get("/cache/session", tags=["cache"], include_in_schema=tracardi.expose_gui_api)
async def get_session_data(session_id: str):
    """
    Returns cache expiration data
    """
    namespace = get_session_key_namespace(session_id, get_context())
    return {"session" : redis_cache.get(session_id, namespace)}
