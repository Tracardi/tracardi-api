from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from tracardi.config import NAME
from tracardi.service.storage.elastic_client import ElasticClient
from elasticsearch import ElasticsearchException
from .auth.permissions import Permissions
from typing import Optional
from hashlib import md5

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.delete("/indices/version/{version}", tags=["index"], include_in_schema=server.expose_gui_api)
async def delete_old_indices(version: str, codename: Optional[str] = None):

    if codename is None:
        codename = md5(version.encode('utf-8')).hexdigest()[:5]

    if codename == NAME:
        raise HTTPException(status_code=409, detail="Cannot delete currently connected indices.")

    try:
        es = ElasticClient.instance()
        indices = await es.list_aliases()
        to_delete = [index for index in indices if index.startswith(f"{version.replace('.', '')}.{codename}.tracardi-")]

        result = {}
        for alias in to_delete:
            result[alias] = await es.remove_index(alias)

        return result

    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
