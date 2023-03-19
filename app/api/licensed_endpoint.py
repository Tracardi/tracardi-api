import logging
from collections import namedtuple

from fastapi import APIRouter, Depends, HTTPException
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from .auth.permissions import Permissions
from ..config import server

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


def get_router(prefix):
    router = APIRouter(
        dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
        prefix=prefix
    )

    @router.get("/{path:path}",
                include_in_schema=server.expose_gui_api)
    async def licensed():
        raise HTTPException(status_code=402, detail="No license. This is licensed feature.")

    @router.post("/{path:path}",
                 include_in_schema=server.expose_gui_api)
    async def licensed():
        raise HTTPException(status_code=402, detail="No license. This is licensed feature.")

    @router.delete("/{path:path}",
                   include_in_schema=server.expose_gui_api)
    async def licensed():
        raise HTTPException(status_code=402, detail="No license. This is licensed feature.")

    @router.put("/{path:path}",
                include_in_schema=server.expose_gui_api)
    async def licensed():
        raise HTTPException(status_code=402, detail="No license. This is licensed feature.")

    endpoint = namedtuple("endpoint", "router")
    return endpoint(router)
