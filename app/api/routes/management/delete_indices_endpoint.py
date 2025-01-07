from fastapi import APIRouter, Depends, HTTPException
from tracardi.config import tracardi
from tracardi.service.dependency import *
from app.api.auth.permissions import Permissions
from typing import Optional

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.delete("/indices", tags=["index"], include_in_schema=tracardi.expose_gui_api)
async def delete_old_indices(db_version: str, codename: Optional[str] = None):

    if db_version == tracardi.version.db_version:
        raise HTTPException(status_code=409, detail="You cannot delete indices that are currently used.")

    indices = await bd_raw_adapter.list_indices()

    # Test
    to_delete = [index for index in indices if index.startswith(
        f"{db_version}.{codename}.tracardi-"
    )]

    # Production
    for index in indices :
        if index.startswith(f"prod-{db_version}.{codename}.tracardi-"):
            to_delete.append(index)

    result = {}
    for alias in to_delete:
        result[alias] = await bd_raw_adapter.remove_index(alias)

    return result
