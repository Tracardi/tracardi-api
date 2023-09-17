from fastapi import APIRouter, Depends, HTTPException
from tracardi.config import tracardi
from tracardi.service.storage.driver.elastic import raw as raw_db
from .auth.permissions import Permissions
from typing import Optional
from tracardi.domain.version import Version

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.delete("/indices/version/{version}", tags=["index"], include_in_schema=tracardi.expose_gui_api)
async def delete_old_indices(version: str, codename: Optional[str] = None):

    version = Version(version=version, name=codename)

    if version == tracardi.version:
        raise HTTPException(status_code=409, detail="You cannot delete indices that are currently used.")

    indices = await raw_db.indices()
    to_delete = [index for index in indices if index.startswith(
        f"{version.get_version_prefix()}.{version.name}.tracardi-"
    )]

    result = {}
    for alias in to_delete:
        result[alias] = await raw_db.remove_index(alias)

    return result
